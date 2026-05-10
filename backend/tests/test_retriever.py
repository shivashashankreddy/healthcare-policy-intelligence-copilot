from langchain_core.documents import Document

from app.retrieval.retriever import retrieve_policy_context


class StubVectorStore:
    def similarity_search_with_relevance_scores(self, query: str, k: int):
        return [(Document(page_content=query, metadata={"source_id": "stub"}), 0.9)]


def test_retriever_delegates_to_vector_store(test_settings, monkeypatch):
    monkeypatch.setattr("app.retrieval.retriever.get_vector_store", lambda settings: StubVectorStore())

    results = retrieve_policy_context("synthetic timely filing question", test_settings)

    assert len(results) == 1
    assert results[0][0].metadata["source_id"] == "stub"
    assert results[0][1] == 0.9
