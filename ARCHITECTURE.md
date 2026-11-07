# Architecture

```mermaid
flowchart TD
    U[User] --> UI[Streamlit UI]
    UI --> A[Assistant Orchestrator]
    A --> P[Mode-specific Prompt]
    A --> T[Career Roadmap / Research Brief Tools]
    A --> R[RAG Retriever]
    R --> X[PDF / DOCX / TXT Extraction]
    X --> C[Chunking]
    C --> E[OpenAI Embeddings]
    E --> V[(Local JSON Vector Store)]
    R --> V
    P --> L[OpenAI Chat API]
    T --> L
    R --> L
    L --> O[Answer + Source Labels]
    O --> UI
```

The orchestrator selects a role prompt, optionally routes the task to a helper tool, retrieves relevant document chunks, and sends the assembled context to the OpenAI chat API. Credentials are read from environment variables or Streamlit Cloud Secrets.
