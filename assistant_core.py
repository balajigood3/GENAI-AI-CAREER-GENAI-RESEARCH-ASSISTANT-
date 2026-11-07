import json
import os
from pathlib import Path
from openai import OpenAI
from document_store import DocumentStore, extract_text

def config(name, default=""):
    value = os.getenv(name)
    if value:
        return value
    try:
        import streamlit as st
        value = st.secrets.get(name, default)
        return str(value) if value else default
    except Exception:
        return default

CHAT_MODEL = config("OPENAI_MODEL", "gpt-4.1-mini")
EMBED_MODEL = config("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
STORE_PATH = Path(config("VECTOR_STORE_PATH", "data/index.json"))

PROMPTS = {
    "Career Coach": "You are an evidence-based AI/ML career coach. Give practical roadmaps, project advice, resume guidance, and measurable milestones. Never invent credentials or experience.",
    "GenAI Researcher": "You are a rigorous GenAI research assistant. Explain methods, compare approaches, identify limitations, and distinguish evidence from speculation. Never fabricate citations.",
    "Document Q&A": "Answer from retrieved uploaded-document passages where possible. Cite sources using [filename]. If evidence is absent, say so and separate general knowledge.",
    "Interview Practice": "Act as a technical interviewer for AI/ML and GenAI roles. Give focused questions, evaluate answers, identify gaps, and provide improved example answers."
}

class CareerResearchAssistant:
    def __init__(self):
        api_key = config("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY is missing. Add it in Streamlit Cloud: Manage app > Settings > Secrets, or in a local .env file.")
        self.client = OpenAI(api_key=api_key)
        self.store = DocumentStore(STORE_PATH)

    def embed(self, texts):
        response = self.client.embeddings.create(model=EMBED_MODEL, input=texts)
        return [x.embedding for x in response.data]

    def index_files(self, files):
        records = []
        for f in files:
            text = extract_text(f.name, f.getvalue())
            for i, chunk in enumerate(self.store.chunk_text(text)):
                records.append({"text": chunk, "source": Path(f.name).name, "chunk": i})
        if not records:
            return 0
        vectors = self.embed([r["text"] for r in records])
        self.store.add(records, vectors)
        return len(records)

    def answer(self, question, mode="Career Coach"):
        retrieved = []
        if self.store.records:
            q_vector = self.embed([question])[0]
            retrieved = self.store.search(q_vector, k=5)
        context = "\n\n".join(f"[{r['source']}] {r['text']}" for r in retrieved)
        tool_output = {"tool": "general_assistance", "result": "No specialized tool selected."}
        q = question.lower()
        if mode == "Career Coach" and any(x in q for x in ("roadmap", "career plan", "learning plan")):
            tool_output = {"tool": "career_roadmap", "result": "Structure the response into weekly goals, skills, portfolio milestones, and measurable acceptance criteria."}
        elif mode == "GenAI Researcher" and any(x in q for x in ("research", "paper", "literature", "survey")):
            tool_output = {"tool": "research_brief", "result": "Structure the response as problem, methods, evidence, evaluation, limitations, and open questions."}

        response = self.client.chat.completions.create(
            model=CHAT_MODEL,
            temperature=0.2,
            messages=[
                {"role": "system", "content": PROMPTS.get(mode, PROMPTS["Career Coach"])},
                {"role": "system", "content": "Retrieved context:\n" + (context or "No relevant uploaded document passages found.") + "\n\nTool result:\n" + json.dumps(tool_output)},
                {"role": "user", "content": question}
            ]
        )
        answer = response.choices[0].message.content or "No response returned."
        if retrieved:
            sources = sorted({r["source"] for r in retrieved})
            answer += "\n\n**Retrieved sources:** " + ", ".join(f"`{s}`" for s in sources)
        return answer
