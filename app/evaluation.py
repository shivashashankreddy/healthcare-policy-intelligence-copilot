import json
from pathlib import Path

from app.config import Settings
from app.rag import answer_query
from app.schemas import EvaluationResponse, EvaluationResult, QueryRequest, Role


SAMPLE_QUESTIONS = [
    {
        "question": "What documentation is required before approving advanced imaging prior authorization?",
        "role": Role.clinical_documentation_reviewer,
        "expected_sources": ["prior_authorization_imaging"],
    },
    {
        "question": "When should a claim be denied for timely filing in the synthetic policy set?",
        "role": Role.claims_analyst,
        "expected_sources": ["claims_timely_filing"],
    },
    {
        "question": "What should a compliance reviewer verify before using AI-generated policy answers?",
        "role": Role.compliance_reviewer,
        "expected_sources": ["ai_compliance_controls"],
    },
]


def run_evaluation(settings: Settings) -> EvaluationResponse:
    results: list[EvaluationResult] = []
    for sample in SAMPLE_QUESTIONS:
        request = QueryRequest(question=sample["question"], query=sample["question"], role=sample["role"])
        response = answer_query(request, settings)
        cited_sources = [citation.source_id for citation in response.citations]
        passed = any(source in cited_sources for source in sample["expected_sources"])
        results.append(
            EvaluationResult(
                question=sample["question"],
                role=sample["role"],
                expected_sources=sample["expected_sources"],
                cited_sources=cited_sources,
                passed=passed,
                risk_flags=response.risk_flags,
            )
        )

    report_dir = Path("reports")
    report_dir.mkdir(parents=True, exist_ok=True)
    json_path = report_dir / "rag_evaluation.json"
    md_path = report_dir / "rag_evaluation.md"
    payload = {
        "total_questions": len(results),
        "passed": sum(result.passed for result in results),
        "failed": sum(not result.passed for result in results),
        "results": [result.model_dump(mode="json") for result in results],
    }
    json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    md_path.write_text(_markdown_report(payload), encoding="utf-8")
    return EvaluationResponse(**payload, report_path=str(md_path), json_path=str(json_path))


def _markdown_report(payload: dict) -> str:
    lines = [
        "# RAG Evaluation Report",
        "",
        f"Total questions: {payload['total_questions']}",
        f"Passed: {payload['passed']}",
        f"Failed: {payload['failed']}",
        "",
        "| Question | Expected Sources | Cited Sources | Passed |",
        "| --- | --- | --- | --- |",
    ]
    for result in payload["results"]:
        lines.append(
            "| {question} | {expected} | {cited} | {passed} |".format(
                question=result["question"],
                expected=", ".join(result["expected_sources"]),
                cited=", ".join(result["cited_sources"]),
                passed=result["passed"],
            )
        )
    return "\n".join(lines) + "\n"
