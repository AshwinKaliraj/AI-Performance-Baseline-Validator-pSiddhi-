from fastapi import APIRouter

from app.services import mlflow_service


router = APIRouter(
    prefix="/mlflow",
    tags=["MLflow"]
)


@router.get("/versions")
def get_baseline_versions():

    return mlflow_service.get_baseline_versions()


@router.get("/compare")
def compare_baselines():

    return mlflow_service.compare_baseline_versions()