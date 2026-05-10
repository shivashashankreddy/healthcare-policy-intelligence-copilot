from langchain_core.documents import Document

from app.core.config import Settings
from app.retrieval.vector_store import get_vector_store


def retrieve_policy_context(query: str, settings: Settings) -> list[tuple[Document, float]]:
    vector_store = get_vector_store(settings)
    return vector_store.similarity_search_with_relevance_scores(
        query,
        k=settings.retrieval_k,
    )
