import json

from app.models.schemas import QueryRequest, QueryResponse, Role
from app.services.audit_service import read_audit_events, write_audit_event


def test_audit_log_hashes_and_sanitizes_query(test_settings):
    request = QueryRequest(
        query="What is required for synthetic timely filing reconsideration?",
        role=Role.claims_analyst,
    )
    response = QueryResponse(
        answer="Synthetic answer",
        role=Role.claims_analyst,
        citations=[],
        risk_flags=[],
        retrieval_confidence=0.4,
    )

    event_id = write_audit_event(request, response, test_settings.audit_log_path)
    events = read_audit_events(test_settings.audit_log_path, limit=10)

    assert events[0]["event_id"] == event_id
    assert events[0]["query_hash"] != request.query
    assert "What is required" in events[0]["query_preview"]
    assert json.loads(test_settings.audit_log_path.read_text(encoding="utf-8").splitlines()[0])
