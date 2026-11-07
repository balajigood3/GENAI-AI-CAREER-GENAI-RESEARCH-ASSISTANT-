import io
import json
import re
from pathlib import Path
import numpy as np

def extract_text(filename, content):
    suffix = Path(filename).suffix.lower()
    if suffix == ".txt":
        return content.decode("utf-8", errors="ignore")
    if suffix == ".pdf":
        from pypdf import PdfReader
        reader = PdfReader(io.BytesIO(content))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    if suffix == ".docx":
        from docx import Document
        doc = Document(io.BytesIO(content))
        return "\n".join(p.text for p in doc.paragraphs)
    raise ValueError(f"Unsupported file type: {suffix}")

class DocumentStore:
    def __init__(self, path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        try:
            self.records = json.loads(self.path.read_text(encoding="utf-8")) if self.path.exists() else []
        except (OSError, json.JSONDecodeError):
            self.records = []

    @staticmethod
    def chunk_text(text, size=900, overlap=150):
        words = re.findall(r"\S+", text)
        chunks, start = [], 0
        while start < len(words):
            chunks.append(" ".join(words[start:start + size]))
            start += max(1, size - overlap)
        return chunks

    def add(self, records, vectors):
        self.records.extend({**r, "embedding": v} for r, v in zip(records, vectors))
        self.path.write_text(json.dumps(self.records), encoding="utf-8")

    def search(self, query_vector, k=5):
        q = np.asarray(query_vector, dtype=float)
        scored = []
        for r in self.records:
            v = np.asarray(r["embedding"], dtype=float)
            denom = np.linalg.norm(q) * np.linalg.norm(v)
            score = float(np.dot(q, v) / denom) if denom else 0.0
            scored.append((score, r))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [r for score, r in scored[:k] if score > 0]
