from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field, field_validator


class Role(StrEnum):
    caseworker = "caseworker"
    claims_analyst = "claims_analyst"
    compliance_reviewer = "compliance_reviewer"
    clinical_documentation_reviewer = "clinical_documentation_reviewer"


class RiskFlag(StrEnum):
    low_retrieval_confidence = "LOW_RETRIEVAL_CONFIDENCE"
    missing_citations = "MISSING_CITATIONS"
    possible_policy_ambiguity = "POSSIBLE_POLICY_AMBIGUITY"
    unsupported_answer = "UNSUPPORTED_ANSWER"


class IngestionRequest(BaseModel):
    reset_collection: bool = Field(default=False)


class IngestionResponse(BaseModel):
    documents_loaded: int
    chunks_indexed: int
    collection_name: str


class QueryRequest(BaseModel):
    query: str = Field(min_length=8, max_length=1200)
    role: Role
    include_audit: bool = True

    @field_validator("query")
    @classmethod
    def reject_sensitive_query(cls, value: str) -> str:
        lowered = value.lower()
        blocked_tokens = ["ssn", "social security", "member id", "patient name", "dob:"]
        if any(token in lowered for token in blocked_tokens):
            raise ValueError("Queries must not include PHI, PII, member identifiers, or patient data.")
        return value


class SourceCitation(BaseModel):
    source_id: str
    title: str
    document_type: str
    section: str
    effective_date: str
    confidence: float


class QueryResponse(BaseModel):
    answer: str
    role: Role
    citations: list[SourceCitation]
    risk_flags: list[RiskFlag]
    retrieval_confidence: float
    audit_event_id: str | None = None


class HealthResponse(BaseModel):
    status: str
    app_name: str
    environment: str


class EvaluationResult(BaseModel):
    question: str
    role: Role
    expected_sources: list[str]
    cited_sources: list[str]
    passed: bool
    risk_flags: list[RiskFlag]


class EvaluationResponse(BaseModel):
    total_questions: int
    passed: int
    failed: int
    results: list[EvaluationResult]
    report_path: str
    json_path: str


class AuditEvent(BaseModel):
    event_id: str
    timestamp_utc: str
    role: Role
    query_hash: str
    query_preview: str
    retrieval_confidence: float
    risk_flags: list[str]
    cited_sources: list[str]


class AuditReviewResponse(BaseModel):
    events: list[dict[str, Any]]
