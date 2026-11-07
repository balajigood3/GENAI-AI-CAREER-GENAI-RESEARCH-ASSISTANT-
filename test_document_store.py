from document_store import DocumentStore

def test_chunk_text_creates_chunks():
    text = " ".join(f"word{i}" for i in range(2200))
    chunks = DocumentStore.chunk_text(text, size=500, overlap=50)
    assert len(chunks) >= 4
    assert all(chunks)

def test_empty_text():
    assert DocumentStore.chunk_text("") == []
