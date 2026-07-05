from fastapi import APIRouter

from app.models.anomaly import AnomalyRequest,AnomalyResponse

from app.services import anomaly_service

router=APIRouter(
    prefix="/anomaly",
    tags=["Anomaly"]
)


@router.post("/",response_model=AnomalyResponse)

def detect_anomaly(request:AnomalyRequest):

    return anomaly_service.detect_anomaly(request.current_value)