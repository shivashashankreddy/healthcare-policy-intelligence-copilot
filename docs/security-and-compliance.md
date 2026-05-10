# Security and Compliance Notes

This repository is designed for portfolio demonstration and local experimentation only. It is not a clinical, payment, compliance, or benefit-determination system.

## Synthetic Data Only

Do not use real PHI, PII, patient records, payer member identifiers, client data, proprietary payer policies, or production claims data.

The included documents are synthetic examples created for software demonstration. They are not derived from real payer manuals, medical records, claims files, client deliverables, or confidential operating procedures.

## Audit Logging

The audit log stores:

- Event ID
- UTC timestamp
- Role
- Query hash
- Sanitized query preview
- Retrieval confidence
- Risk flags
- Synthetic cited source IDs

It does not intentionally store full prompts, full user queries, patient data, member IDs, or model transcripts.

## Guardrails

The system returns cautious responses when retrieval confidence is low and flags missing citations, ambiguous policy context, and unsupported answers.

These guardrails are decision-support controls, not guarantees. A production healthcare deployment would also require authentication, authorization, data loss prevention, access logging, retention policies, human review, model monitoring, and formal compliance review.
