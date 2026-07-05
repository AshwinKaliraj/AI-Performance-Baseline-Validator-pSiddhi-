from fastapi import APIRouter
print("Baseline router loaded")

from app.services import baseline_service

from app.models.baseline import BaselineResponse

router=APIRouter(
    prefix="/baseline",
    tags=["Baseline"]
)

@router.get("/",response_model=BaselineResponse)

def get_baseline():

    return baseline_service.calculate_baseline()