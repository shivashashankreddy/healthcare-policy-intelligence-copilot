from fastapi import APIRouter

from app.core.config import get_settings
from app.models.schemas import AuditReviewResponse
from app.services.audit_service import read_audit_events

router = APIRouter(tags=["audit"])


@router.get("/audit", response_model=AuditReviewResponse)
def audit(limit: int | None = None) -> AuditReviewResponse:
    settings = get_settings()
    event_limit = limit or settings.max_audit_events
    return AuditReviewResponse(events=read_audit_events(settings.audit_log_path, limit=event_limit))
