from fastapi import APIRouter

from app.models.analyze import AnalyzeRequest,AnalyzeResponse

from app.services import analyze_service


router=APIRouter(

    prefix="/analyze",

    tags=["AI Analysis"]

)


@router.post("/",response_model=AnalyzeResponse)

def analyze(request:AnalyzeRequest):

    return analyze_service.analyze(request.current_value)