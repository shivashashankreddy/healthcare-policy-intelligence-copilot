from collections.abc import Generator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.core.config import Settings, get_settings
from app.main import app


@pytest.fixture()
def test_settings(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Settings:
    settings = Settings(
        data_dir=tmp_path / "data",
        policy_docs_dir=Path("sample-data"),
        chroma_dir=tmp_path / "chroma",
        audit_log_path=tmp_path / "logs" / "query_audit.jsonl",
        min_retrieval_score=0.0,
    )
    get_settings.cache_clear()
    monkeypatch.setattr("app.core.config.get_settings", lambda: settings)
    monkeypatch.setattr("app.api.health.get_settings", lambda: settings)
    monkeypatch.setattr("app.api.ingest.get_settings", lambda: settings)
    monkeypatch.setattr("app.api.query.get_settings", lambda: settings)
    monkeypatch.setattr("app.api.evaluation.get_settings", lambda: settings)
    monkeypatch.setattr("app.api.audit.get_settings", lambda: settings)
    return settings


@pytest.fixture()
def client(test_settings: Settings) -> Generator[TestClient, None, None]:
    with TestClient(app) as test_client:
        yield test_client
