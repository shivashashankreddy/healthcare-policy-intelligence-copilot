# Healthcare Policy Intelligence Copilot

Production-style Healthcare Claims and Policy RAG Copilot built with Python, FastAPI, LangChain, local embeddings, Chroma, synthetic healthcare policy documents, Pytest, Docker, and GitHub Actions.

The goal is to show how an enterprise GenAI service can support healthcare operations teams with grounded, cited, role-aware policy answers while keeping strict boundaries around PHI, PII, payer member data, proprietary payer content, and real client data.

## Business Problem

Healthcare operations teams frequently need to interpret prior authorization, claims, appeals, documentation, and compliance policies under time pressure. A generic chatbot is not enough for this workflow because users need source citations, confidence signals, auditability, role-specific guidance, and safe behavior when retrieved policy evidence is weak.

This copilot is designed as a local-first reference implementation for:

- Caseworkers who need plain-language next steps.
- Claims analysts who need adjudication and denial-rule support.
- Compliance reviewers who need auditability and AI governance checks.
- Clinical documentation reviewers who need policy-backed documentation gap analysis.

## Architecture Summary

```text
Synthetic Markdown Policies
        |
        v
LangChain Loader + Chunker
        |
        v
Local Embeddings -> Chroma Vector Store
        |
        v
FastAPI RAG Service
        |
        +--> Role-aware prompt templates
        +--> Source citation metadata
        +--> Hallucination guardrails
        +--> JSONL audit logs
        +--> Lightweight RAG evaluation
```

The system uses local embeddings by default and can run without paid API keys. A deterministic grounded-answer layer is included so the project remains runnable in local and CI environments while preserving the same control points a hosted LLM adapter would use in production.

## API Endpoints

| Method | Endpoint | Purpose |
| --- | --- | --- |
| `GET` | `/health` | Service health check |
| `POST` | `/ingest` | Index synthetic policy documents |
| `POST` | `/query` | Role-aware RAG query with citations and risk flags |
| `POST` | `/evaluate` | Run sample RAG evaluation and write reports |
| `GET` | `/audit` | Review sanitized local audit events |

Ingest the synthetic policy corpus:

```bash
curl -X POST http://localhost:8000/ingest \
  -H "Content-Type: application/json" \
  -d '{"reset_collection": true}'
```

Ask a role-aware question:

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What documentation is required before approving advanced imaging prior authorization?",
    "role": "clinical_documentation_reviewer",
    "include_audit": true
  }'
```

Response shape:

```json
{
  "answer": "In clinical_documentation_reviewer mode, the synthetic policy context supports...",
  "role": "clinical_documentation_reviewer",
  "citations": [
    {
      "source_id": "prior_authorization_imaging",
      "title": "Synthetic Prior Authorization Policy for Advanced Imaging",
      "document_type": "prior_authorization",
      "section": "Clinical Documentation Criteria",
      "effective_date": "2026-01-01",
      "confidence": 0.87
    }
  ],
  "risk_flags": ["POSSIBLE_POLICY_AMBIGUITY"],
  "retrieval_confidence": 0.87,
  "audit_event_id": "generated-event-id"
}
```

Supported roles:

- `caseworker`
- `claims_analyst`
- `compliance_reviewer`
- `clinical_documentation_reviewer`

## Risk Flags

Responses can include:

- `LOW_RETRIEVAL_CONFIDENCE`
- `MISSING_CITATIONS`
- `POSSIBLE_POLICY_AMBIGUITY`
- `UNSUPPORTED_ANSWER`

When retrieval confidence is low, the copilot returns a cautious response instead of inventing unsupported policy guidance.

## Security Notes

This repository uses only synthetic policy, prior authorization, claims, appeals, operations, and compliance documents. It is designed for portfolio demonstration and local experimentation, not production clinical, payment, or benefit determinations.

Do not ingest or paste:

- PHI or PII
- Patient names
- Member IDs
- SSNs
- Real claims data
- Real payer data
- Real client documents
- Proprietary policy manuals

Audit logs are written to local JSONL files and store only query hashes, sanitized previews, roles, timestamps, retrieval confidence, risk flags, and synthetic cited source IDs. The application does not intentionally persist full prompts, full raw queries, patient records, model transcripts, or real-world identifiers.

## Local Development

Create a virtual environment and install dependencies:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r backend/requirements-dev.txt
```

Run the API:

```bash
uvicorn app.main:app --app-dir backend --reload
```

Ingest synthetic policies on Windows PowerShell:

```bash
curl -X POST http://localhost:8000/ingest ^
  -H "Content-Type: application/json" ^
  -d "{\"reset_collection\": true}"
```

Query the API on Windows PowerShell:

```bash
curl -X POST http://localhost:8000/query ^
  -H "Content-Type: application/json" ^
  -d "{\"query\":\"What documentation is required before approving advanced imaging prior authorization?\",\"role\":\"clinical_documentation_reviewer\",\"include_audit\":true}"
```

Run tests:

```bash
python -m pytest
```

Run linting:

```bash
ruff check backend scripts
```

## Docker

```bash
docker compose up --build
```

The API will be available at `http://localhost:8000`.

## Evaluation Approach

The lightweight evaluator asks sample role-aware questions and checks whether expected synthetic source documents appear in citations. This gives the project a repeatable signal for retrieval quality without depending on paid model evaluation services.

Outputs:

- `reports/rag_evaluation.json`
- `reports/rag_evaluation.md`

This is intentionally simple for version 1. A production implementation would add curated golden datasets, retrieval recall metrics, answer faithfulness scoring, citation precision, regression thresholds, human review workflows, and monitoring dashboards.

## Repository Structure

```text
backend/
  app/                FastAPI application package
  app/api/            Route modules for health, ingestion, query, evaluation, and audit
  app/core/           Configuration and security helpers
  app/models/         Pydantic schemas
  app/prompts/        Grounded answer prompt templates
  app/retrieval/      Document loading, vector store, and retriever logic
  app/services/       RAG, evaluation, guardrail, and audit services
  tests/              Backend unit tests
  Dockerfile          Backend container image
sample-data/          Synthetic healthcare policy markdown files
docs/                 Architecture, API design, evaluation, security, and deployment docs
docs/adr/             Architecture decision records
scripts/              Local ingestion and evaluation scripts
diagrams/             Mermaid architecture diagram
.github/workflows/   GitHub Actions CI
```

## Limitations

- Version 1 does not include a frontend.
- The answer generator is deterministic and local-first, so the repo runs without API keys.
- Synthetic documents are intentionally small.
- Chroma is configured for local development, not multi-tenant production serving.
- Role modes guide response behavior but do not implement user authentication or authorization.

## Future Enhancements

- Add an LLM provider interface for OpenAI, Azure OpenAI, Bedrock, or local model servers.
- Add authentication, RBAC, and role-specific document access rules.
- Add async ingestion jobs and document versioning.
- Add citation-level evaluation and hallucination scoring.
- Add policy update workflows with reviewer approval.
- Add observability dashboards for retrieval confidence and risk flag trends.
