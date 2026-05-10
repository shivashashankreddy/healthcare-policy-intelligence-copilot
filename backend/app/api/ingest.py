from fastapi import APIRouter

from app.core.config import get_settings
from app.models.schemas import IngestionRequest, IngestionResponse
from app.retrieval.document_loader import load_synthetic_documents
from app.retrieval.vector_store import COLLECTION_NAME, ingest_documents

router = APIRouter(tags=["ingestion"])


@router.post("/ingest", response_model=IngestionResponse)
def ingest(request: IngestionRequest) -> IngestionResponse:
    settings = get_settings()
    documents = load_synthetic_documents(settings.policy_docs_dir)
    chunks = ingest_documents(documents, settings, reset=request.reset_collection)
    return IngestionResponse(
        documents_loaded=len(documents),
        chunks_indexed=chunks,
        collection_name=COLLECTION_NAME,
    )
