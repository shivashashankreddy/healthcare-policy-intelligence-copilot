# API Reference

Run locally:

```bash
uvicorn app.main:app --reload
```

## GET /health

Returns service health metadata.

Example:

```bash
curl http://localhost:8000/health
```

## POST /ingest

Indexes synthetic markdown policy documents.

Request:

```json
{
  "reset_collection": true
}
```

Example:

```bash
curl -X POST http://localhost:8000/ingest \
  -H "Content-Type: application/json" \
  -d '{"reset_collection": true}'
```

## POST /query

Runs role-aware RAG with citations, retrieval confidence, risk flags, and optional audit logging.

Request:

```json
{
  "query": "What documentation is required before approving advanced imaging prior authorization?",
  "role": "clinical_documentation_reviewer",
  "include_audit": true
}
```

Example:

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "When should a claim be denied for timely filing in the synthetic policy set?",
    "role": "claims_analyst",
    "include_audit": true
  }'
```

Response fields:

- `answer`: Grounded answer generated from retrieved synthetic policy context.
- `citations`: Source metadata for retrieved documents.
- `risk_flags`: Guardrail signals such as low retrieval confidence or missing citations.
- `retrieval_confidence`: Aggregate retrieval confidence score.
- `audit_event_id`: Local audit event identifier when audit logging is enabled.

Supported roles:

- `caseworker`
- `claims_analyst`
- `compliance_reviewer`
- `clinical_documentation_reviewer`

## POST /evaluate

Runs lightweight retrieval evaluation and writes JSON and markdown reports under `reports/`.

Example:

```bash
curl -X POST http://localhost:8000/evaluate
```

## GET /audit

Returns recent sanitized audit events from local JSONL storage.

Example:

```bash
curl "http://localhost:8000/audit?limit=25"
```
