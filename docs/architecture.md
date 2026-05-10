# Architecture

The Healthcare Policy Intelligence Copilot is a local-first RAG service for synthetic healthcare policy workflows. It is designed to look and behave like an enterprise GenAI backend while remaining safe to run in public portfolio and interview environments.

## Design Goals

- Run locally without paid API keys.
- Use only synthetic healthcare policy documents.
- Return answers grounded in retrieved source metadata.
- Provide role-aware behavior for realistic operations workflows.
- Prefer cautious responses when retrieval evidence is weak.
- Keep audit logs useful without storing sensitive data.

## Components

- FastAPI exposes health, ingestion, query, evaluation, and audit review endpoints.
- Synthetic markdown documents represent prior authorization, claims, appeals, operations, and compliance policies.
- LangChain document utilities load and chunk policy content.
- Chroma stores local vectors with source citation metadata.
- SentenceTransformers provides local embeddings by default, with a deterministic fake-embedding fallback for constrained environments.
- Role-aware prompting adapts answer style for caseworkers, claims analysts, compliance reviewers, and clinical documentation reviewers.
- Guardrails flag low retrieval confidence, missing citations, ambiguous policy language, and unsupported answers.
- Audit logging writes JSONL records with hashed queries and sanitized previews.

See `diagrams/architecture.mmd` for the Mermaid architecture diagram used to explain the system in interviews and portfolio walkthroughs.

## Request Flow

```text
POST /query
    |
    v
Validate role and query schema
    |
    v
Retrieve synthetic policy chunks from Chroma
    |
    v
Build grounded role-aware prompt context
    |
    v
Generate deterministic local answer
    |
    v
Attach citations, confidence, and risk flags
    |
    v
Write sanitized audit event when enabled
```

## Production Extension Points

- Replace deterministic answer synthesis with an LLM provider adapter.
- Add authentication, RBAC, and role-specific document filtering.
- Add document versioning and reviewer-approved policy publishing.
- Add observability for retrieval confidence, risk flags, and citation coverage.
- Add human review workflows for unsupported or ambiguous answers.

## Data Boundaries

This project is intentionally synthetic. Do not ingest PHI, PII, payer member data, patient records, proprietary payer policies, or real client documentation.
