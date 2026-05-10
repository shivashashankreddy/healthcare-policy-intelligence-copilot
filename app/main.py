from fastapi import FastAPI

from app.audit import read_audit_events, write_audit_event
from app.config import get_settings
from app.document_loader import load_synthetic_documents
from app.evaluation import run_evaluation
from app.rag import answer_query
from app.schemas import (
    AuditReviewResponse,
    EvaluationResponse,
    HealthResponse,
    IngestionRequest,
    IngestionResponse,
    QueryRequest,
    QueryResponse,
)
from app.vector_store import COLLECTION_NAME, ingest_documents

settings = get_settings()
app = FastAPI(
    title=settings.app_name,
    description="Enterprise-style RAG copilot for synthetic healthcare claims and policy workflows.",
    version="0.1.0",
)


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(
        status="ok",
        app_name=settings.app_name,
        environment=settings.environment,
    )


@app.post("/ingest", response_model=IngestionResponse)
def ingest(request: IngestionRequest) -> IngestionResponse:
    documents = load_synthetic_documents(settings.policy_docs_dir)
    chunks = ingest_documents(documents, settings, reset=request.reset_collection)
    return IngestionResponse(
        documents_loaded=len(documents),
        chunks_indexed=chunks,
        collection_name=COLLECTION_NAME,
    )


@app.post("/query", response_model=QueryResponse)
def query(request: QueryRequest) -> QueryResponse:
    response = answer_query(request, settings)
    if request.include_audit:
        event_id = write_audit_event(request, response, settings.audit_log_path)
        response.audit_event_id = event_id
    return response


@app.post("/evaluate", response_model=EvaluationResponse)
def evaluate() -> EvaluationResponse:
    return run_evaluation(settings)


@app.get("/audit", response_model=AuditReviewResponse)
def audit(limit: int = settings.max_audit_events) -> AuditReviewResponse:
    return AuditReviewResponse(events=read_audit_events(settings.audit_log_path, limit=limit))
