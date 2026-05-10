from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Healthcare Policy Intelligence Copilot"
    environment: str = "local"
    data_dir: Path = Path("backend/data")
    policy_docs_dir: Path = Path("sample-data")
    chroma_dir: Path = Path("backend/data/chroma")
    audit_log_path: Path = Path("logs/query_audit.jsonl")
    embedding_model_name: str = "sentence-transformers/all-MiniLM-L6-v2"
    retrieval_k: int = 4
    min_retrieval_score: float = 0.22
    max_audit_events: int = 100

    model_config = SettingsConfigDict(env_file=".env", env_prefix="HCPC_")


@lru_cache
def get_settings() -> Settings:
    return Settings()
