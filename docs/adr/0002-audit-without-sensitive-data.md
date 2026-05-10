# ADR 0002: Audit Logging Without Sensitive Data

## Status

Accepted

## Context

Healthcare AI systems need traceability, but storing raw prompts or user data can create privacy and compliance risk.

## Decision

Write local JSONL audit events containing role, timestamp, query hash, sanitized preview, risk flags, retrieval confidence, and synthetic cited source IDs.

## Consequences

The system supports reviewability while reducing data retention risk. This is suitable for a portfolio project and can be extended with centralized logging, retention policies, access control, and immutable audit storage.
