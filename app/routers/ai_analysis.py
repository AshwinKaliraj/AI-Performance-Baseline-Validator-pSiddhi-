from fastapi import APIRouter
from app.services import ai_summary_service

router = APIRouter(
    prefix="/ai-analysis",
    tags=["AI Analysis"]
)

@router.get("/")
def get_analysis():
    return ai_summary_service.get()