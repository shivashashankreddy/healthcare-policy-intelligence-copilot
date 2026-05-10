from app.guardrails import evaluate_risks
from app.schemas import RiskFlag


def test_low_confidence_guardrail_flags_unsupported_answer():
    flags = evaluate_risks(
        answer="The available synthetic policy context is insufficient.",
        citations=[],
        retrieval_confidence=0.01,
        min_confidence=0.2,
        context="",
    )

    assert RiskFlag.low_retrieval_confidence in flags
    assert RiskFlag.missing_citations in flags
    assert RiskFlag.unsupported_answer in flags


def test_ambiguity_guardrail_flags_policy_ambiguity():
    flags = evaluate_risks(
        answer="This may require escalation.",
        citations=[],
        retrieval_confidence=0.5,
        min_confidence=0.2,
        context="Exceptions may be considered case-by-case.",
    )

    assert RiskFlag.possible_policy_ambiguity in flags
