import os
from pathlib import Path

os.environ.setdefault("USE_TF", "0")

from langchain_community.embeddings import FakeEmbeddings, HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.core.config import Settings

COLLECTION_NAME = "synthetic_healthcare_policy_docs"


def build_embeddings(settings: Settings):
    try:
        return HuggingFaceEmbeddings(model_name=settings.embedding_model_name)
    except Exception:
        return FakeEmbeddings(size=384)


def get_vector_store(settings: Settings) -> Chroma:
    settings.chroma_dir.mkdir(parents=True, exist_ok=True)
    return Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=build_embeddings(settings),
        persist_directory=str(settings.chroma_dir),
    )


def chunk_documents(documents: list[Document]) -> list[Document]:
    splitter = RecursiveCharacterTextSplitter(chunk_size=900, chunk_overlap=120)
    chunks = splitter.split_documents(documents)
    for index, chunk in enumerate(chunks):
        chunk.metadata["chunk_id"] = f"{chunk.metadata.get('source_id', 'doc')}::chunk-{index}"
    return chunks


def ingest_documents(documents: list[Document], settings: Settings, reset: bool = False) -> int:
    if reset and Path(settings.chroma_dir).exists():
        import shutil

        shutil.rmtree(settings.chroma_dir)

    vector_store = get_vector_store(settings)
    chunks = chunk_documents(documents)
    if chunks:
        vector_store.add_documents(chunks)
        vector_store.persist()
    return len(chunks)
