import pytest
from pydantic import ValidationError

from app.schemas import QueryRequest, Role


def test_query_schema_accepts_supported_roles():
    request = QueryRequest(
        query="What documentation is required for synthetic imaging authorization?",
        role=Role.clinical_documentation_reviewer,
    )

    assert request.role == Role.clinical_documentation_reviewer


def test_query_schema_rejects_sensitive_tokens():
    with pytest.raises(ValidationError):
        QueryRequest(query="Use SSN 123-45-6789 to find the claim", role=Role.claims_analyst)
