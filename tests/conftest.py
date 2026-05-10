from collections.abc import Generator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.config import Settings
from app.main import app


@pytest.fixture()
def test_settings(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Settings:
    settings = Settings(
        data_dir=tmp_path / "data",
        policy_docs_dir=Path("data/synthetic_policy_docs"),
        chroma_dir=tmp_path / "chroma",
        audit_log_path=tmp_path / "logs" / "query_audit.jsonl",
        min_retrieval_score=0.0,
    )
    monkeypatch.setattr("app.main.settings", settings)
    return settings


@pytest.fixture()
def client(test_settings: Settings) -> Generator[TestClient, None, None]:
    with TestClient(app) as test_client:
        yield test_client
