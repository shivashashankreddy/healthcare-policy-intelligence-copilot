from app.schemas import RiskFlag, SourceCitation


AMBIGUITY_TERMS = ["may", "case-by-case", "exceptions", "unless", "clinical judgment"]


def evaluate_risks(
    answer: str,
    citations: list[SourceCitation],
    retrieval_confidence: float,
    min_confidence: float,
    context: str,
) -> list[RiskFlag]:
    flags: list[RiskFlag] = []
    if retrieval_confidence < min_confidence:
        flags.append(RiskFlag.low_retrieval_confidence)
    if not citations:
        flags.append(RiskFlag.missing_citations)
    if any(term in context.lower() for term in AMBIGUITY_TERMS):
        flags.append(RiskFlag.possible_policy_ambiguity)
    if "insufficient" in answer.lower() or retrieval_confidence < min_confidence / 2:
        flags.append(RiskFlag.unsupported_answer)
    return list(dict.fromkeys(flags))


def cautious_answer(question: str) -> str:
    return (
        "The available synthetic policy context is not strong enough to provide a grounded "
        f"answer to: '{question}'. Please ingest or retrieve more specific policy, claims, "
        "appeals, or compliance guidance before using this for operational decision support."
    )
