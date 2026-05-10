import hashlib
import re


SENSITIVE_PATTERNS = [
    re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
    re.compile(r"\b\d{9,12}\b"),
    re.compile(r"\b[A-Z][a-z]+\s+[A-Z][a-z]+\b"),
]


def hash_query(query: str) -> str:
    return hashlib.sha256(query.encode("utf-8")).hexdigest()


def sanitize_query_preview(query: str, limit: int = 120) -> str:
    sanitized = query
    for pattern in SENSITIVE_PATTERNS:
        sanitized = pattern.sub("[REDACTED]", sanitized)
    return sanitized[:limit]
