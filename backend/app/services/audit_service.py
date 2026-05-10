import json
import uuid
from datetime import UTC, datetime

from app.core.security import hash_query, sanitize_query_preview
from app.models.schemas import AuditEvent, QueryRequest, QueryResponse


def write_audit_event(request: QueryRequest, response: QueryResponse, audit_log_path) -> str:
    audit_log_path.parent.mkdir(parents=True, exist_ok=True)
    event_id = str(uuid.uuid4())
    event = AuditEvent(
        event_id=event_id,
        timestamp_utc=datetime.now(UTC).isoformat(),
        role=request.role,
        query_hash=hash_query(request.query),
        query_preview=sanitize_query_preview(request.query),
        retrieval_confidence=response.retrieval_confidence,
        risk_flags=[flag.value for flag in response.risk_flags],
        cited_sources=[citation.source_id for citation in response.citations],
    )
    with audit_log_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event.model_dump(mode="json")) + "\n")
    return event_id


def read_audit_events(audit_log_path, limit: int) -> list[dict]:
    if not audit_log_path.exists():
        return []
    lines = audit_log_path.read_text(encoding="utf-8").splitlines()
    events = [json.loads(line) for line in lines if line.strip()]
    return events[-limit:]
