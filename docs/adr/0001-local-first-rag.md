# ADR 0001: Local-First RAG for Portfolio Demonstration

## Status

Accepted

## Context

The project must run locally without paid API keys and must avoid real healthcare data.

## Decision

Use local embeddings, a local Chroma vector store, synthetic markdown policies, and deterministic grounded answer synthesis.

## Consequences

The repository is easy to run in interviews and CI. It demonstrates architecture, guardrails, and evaluation patterns without requiring external model credentials. The generated answers are less fluent than a hosted LLM, but the design allows a production LLM adapter to be added later.
