# ADR 0003: Role-Aware Policy Answers

## Status

Accepted

## Context

Healthcare operations teams ask different questions depending on job function.

## Decision

Expose explicit role modes for caseworkers, claims analysts, compliance reviewers, and clinical documentation reviewers. Each role changes prompt guidance while preserving shared retrieval and citation rules.

## Consequences

The system demonstrates enterprise workflow awareness without creating separate applications per team. Future versions can add authorization, role-specific retrieval filters, and response approval workflows.
