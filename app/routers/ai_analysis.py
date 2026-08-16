from fastapi import APIRouter

from app.services import ai_summary_service
from app.services import mlflow_service


router = APIRouter(
    prefix="/ai-analysis",
    tags=["AI Analysis"]
)


@router.get("/")
def get_analysis():

    return ai_summary_service.get()


@router.get("/mlflow/versions")
def get_mlflow_versions():

    return mlflow_service.get_baseline_versions()


@router.get("/mlflow/compare")
def compare_mlflow_baselines():

    return mlflow_service.compare_baseline_versions()