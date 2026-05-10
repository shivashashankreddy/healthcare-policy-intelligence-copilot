from fastapi import APIRouter

from app.core.config import get_settings
from app.models.schemas import QueryRequest, QueryResponse
from app.services.audit_service import write_audit_event
from app.services.rag_service import answer_query

router = APIRouter(tags=["query"])


@router.post("/query", response_model=QueryResponse)
def query(request: QueryRequest) -> QueryResponse:
    settings = get_settings()
    response = answer_query(request, settings)
    if request.include_audit:
        event_id = write_audit_event(request, response, settings.audit_log_path)
        response.audit_event_id = event_id
    return response
