from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))

from app.core.config import get_settings
from app.retrieval.document_loader import load_synthetic_documents
from app.retrieval.vector_store import COLLECTION_NAME, ingest_documents


def main() -> None:
    settings = get_settings()
    documents = load_synthetic_documents(settings.policy_docs_dir)
    chunks = ingest_documents(documents, settings, reset=True)
    print(
        f"Indexed {chunks} chunks from {len(documents)} synthetic documents "
        f"into collection '{COLLECTION_NAME}'."
    )


if __name__ == "__main__":
    main()
