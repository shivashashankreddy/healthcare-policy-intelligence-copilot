from app.document_loader import load_synthetic_documents
from app.vector_store import chunk_documents


def test_loads_and_chunks_synthetic_documents(test_settings):
    documents = load_synthetic_documents(test_settings.policy_docs_dir)
    chunks = chunk_documents(documents)

    assert len(documents) >= 5
    assert len(chunks) >= len(documents)
    assert all("source_id" in chunk.metadata for chunk in chunks)
