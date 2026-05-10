from langchain_core.documents import Document

from app.config import Settings
from app.guardrails import cautious_answer, evaluate_risks
from app.prompts import ANSWER_TEMPLATE, ROLE_INSTRUCTIONS
from app.schemas import QueryRequest, QueryResponse, RiskFlag, SourceCitation
from app.vector_store import get_vector_store


def answer_query(request: QueryRequest, settings: Settings) -> QueryResponse:
    vector_store = get_vector_store(settings)
    docs_with_scores = vector_store.similarity_search_with_relevance_scores(
        request.query,
        k=settings.retrieval_k,
    )
    citations = [_citation_from_doc(doc, score) for doc, score in docs_with_scores if score > 0]
    confidence = _aggregate_confidence([score for _, score in docs_with_scores])
    context = _format_context([doc for doc, _ in docs_with_scores])

    if confidence < settings.min_retrieval_score or not citations:
        answer = cautious_answer(request.query)
    else:
        prompt = ANSWER_TEMPLATE.format(
            role=request.role.value,
            role_instruction=ROLE_INSTRUCTIONS[request.role],
            context=context,
            question=request.query,
        )
        answer = _local_grounded_generation(prompt, citations, request.role.value)

    risk_flags = evaluate_risks(
        answer=answer,
        citations=citations,
        retrieval_confidence=confidence,
        min_confidence=settings.min_retrieval_score,
        context=context,
    )
    if RiskFlag.low_retrieval_confidence in risk_flags and RiskFlag.unsupported_answer not in risk_flags:
        risk_flags.append(RiskFlag.unsupported_answer)

    return QueryResponse(
        answer=answer,
        role=request.role,
        citations=citations,
        risk_flags=risk_flags,
        retrieval_confidence=confidence,
    )


def _citation_from_doc(doc: Document, score: float) -> SourceCitation:
    metadata = doc.metadata
    return SourceCitation(
        source_id=str(metadata.get("source_id", "unknown")),
        title=str(metadata.get("title", "Untitled synthetic document")),
        document_type=str(metadata.get("document_type", "synthetic_policy")),
        section=str(metadata.get("section", "general")),
        effective_date=str(metadata.get("effective_date", "unknown")),
        confidence=round(max(0.0, min(1.0, float(score))), 4),
    )


def _aggregate_confidence(scores: list[float]) -> float:
    positive_scores = [max(0.0, min(1.0, float(score))) for score in scores if score > 0]
    if not positive_scores:
        return 0.0
    return round(sum(positive_scores[:3]) / min(3, len(positive_scores)), 4)


def _format_context(docs: list[Document]) -> str:
    formatted = []
    for doc in docs:
        metadata = doc.metadata
        formatted.append(
            "[{source_id} | {title} | {section}]\n{content}".format(
                source_id=metadata.get("source_id", "unknown"),
                title=metadata.get("title", "Untitled"),
                section=metadata.get("section", "general"),
                content=doc.page_content,
            )
        )
    return "\n\n".join(formatted)


def _local_grounded_generation(prompt: str, citations: list[SourceCitation], role: str) -> str:
    # This deterministic generator keeps the project runnable without API keys while still
    # exercising the same prompt-grounding path a hosted LLM would use in production.
    context = prompt.split("Grounding context:", 1)[-1].split("User question:", 1)[0].strip()
    source_list = ", ".join(sorted({citation.source_id for citation in citations}))
    relevant_lines = [
        line.strip("- ").strip()
        for line in context.splitlines()
        if line.strip() and not line.startswith("[")
    ][:6]
    synthesized = " ".join(relevant_lines)
    return (
        f"In {role} mode, the synthetic policy context supports the following: "
        f"{synthesized} Sources: {source_list}. Use this as decision support only and verify "
        "against the governing policy before any operational action."
    )
