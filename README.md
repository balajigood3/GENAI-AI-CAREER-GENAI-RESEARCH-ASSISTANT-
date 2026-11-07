# AI Career & GenAI Research Assistant

A Streamlit capstone application demonstrating OpenAI chat completions, prompt engineering, document RAG, embeddings, task routing, and a lightweight agent workflow.

## Modes
- Career Coach: career roadmap, portfolio and resume guidance.
- GenAI Researcher: research briefs, method comparisons and limitations.
- Document Q&A: question answering over uploaded files.
- Interview Practice: technical interview questions and feedback.

## Run locally
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
cp .env.example .env
# Add your NEW API key to .env
streamlit run app.py
```

## Streamlit Cloud secrets
Open Manage app > Settings > Secrets and add:
```toml
OPENAI_API_KEY = "YOUR_NEW_API_KEY"
OPENAI_MODEL = "gpt-4.1-mini"
OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"
VECTOR_STORE_PATH = "data/index.json"
```

## RAG pipeline
Extract PDF/DOCX/TXT text -> overlapping chunks -> OpenAI embeddings -> local JSON vector store -> cosine-similarity retrieval -> grounded LLM prompt.

## Security
Never commit `.env`, Streamlit secrets, API keys, or private documents. Any API key pasted into chat, source control, or screenshots should be revoked and replaced. The project reads secrets at runtime; it does not embed credentials in source code.

## GitHub
```bash
git init
git add .
git commit -m "Build AI career and GenAI research assistant"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/genai-career-research-assistant.git
git push -u origin main
```

## Deployment
Deploy `app.py` with Streamlit Community Cloud and configure the secrets above. This is a learning/demo implementation; add authentication, tenant isolation, production vector storage, evaluation, monitoring, and privacy controls before real-world use.
