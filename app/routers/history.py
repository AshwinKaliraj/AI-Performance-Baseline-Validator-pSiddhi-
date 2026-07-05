from fastapi import APIRouter

from app.models.history import HistoryRequest,HistoryResponse

from app.services import history_service

router=APIRouter(
    prefix="/history",
    tags=["Performance History"]
)


@router.post("/",response_model=HistoryResponse)

def add_history(request:HistoryRequest):

    return history_service.add_history(request.response_time)


@router.get("/")

def get_history():

    return history_service.get_history()