from fastapi import APIRouter

from app.core.config import get_settings
from app.models.schemas import EvaluationResponse
from app.services.evaluation_service import run_evaluation

router = APIRouter(tags=["evaluation"])


@router.post("/evaluate", response_model=EvaluationResponse)
def evaluate() -> EvaluationResponse:
    return run_evaluation(get_settings())
