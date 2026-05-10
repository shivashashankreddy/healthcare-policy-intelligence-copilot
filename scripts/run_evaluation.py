from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))

from app.core.config import get_settings
from app.services.evaluation_service import run_evaluation


def main() -> None:
    result = run_evaluation(get_settings())
    print(
        f"Evaluation complete: {result.passed}/{result.total_questions} passed. "
        f"Markdown report: {result.report_path}"
    )


if __name__ == "__main__":
    main()
