from pathlib import Path

from langchain_core.documents import Document


def load_synthetic_documents(policy_docs_dir: Path) -> list[Document]:
    documents: list[Document] = []
    for path in sorted(policy_docs_dir.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        metadata = _parse_front_matter(text, path)
        body = text.split("---", 2)[-1].strip() if text.startswith("---") else text
        documents.append(Document(page_content=body, metadata=metadata))
    return documents


def _parse_front_matter(text: str, path: Path) -> dict[str, str]:
    metadata = {
        "source_id": path.stem,
        "title": path.stem.replace("_", " ").title(),
        "document_type": "synthetic_policy",
        "section": "general",
        "effective_date": "2026-01-01",
    }
    if not text.startswith("---"):
        return metadata

    parts = text.split("---", 2)
    if len(parts) < 3:
        return metadata

    for line in parts[1].splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip().strip('"')
    return metadata
