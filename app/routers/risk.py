from fastapi import APIRouter

from app.models.risk import RiskRequest,RiskResponse

from app.services import risk_service

router=APIRouter(
    prefix="/risk",
    tags=["Risk"]
)


@router.post("/",response_model=RiskResponse)

def calculate_risk(request:RiskRequest):

    return risk_service.calculate_risk(request.current_value)