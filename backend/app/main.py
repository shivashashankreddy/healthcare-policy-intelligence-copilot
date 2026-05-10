from fastapi import FastAPI

from app.api import audit, evaluation, health, ingest, query
from app.core.config import get_settings

settings = get_settings()
app = FastAPI(
    title=settings.app_name,
    description="Enterprise-style RAG copilot for synthetic healthcare claims and policy workflows.",
    version="0.1.0",
)

app.include_router(health.router)
app.include_router(ingest.router)
app.include_router(query.router)
app.include_router(evaluation.router)
app.include_router(audit.router)
