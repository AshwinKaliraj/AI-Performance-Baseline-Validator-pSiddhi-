from fastapi import APIRouter

from app.models.validation import ValidationRequest,ValidationResponse

from app.services import validation_service

router=APIRouter(
    prefix="/validation",
    tags=["Validation"]
)


@router.post("/",response_model=ValidationResponse)

def validate(request:ValidationRequest):

    return validation_service.validate_performance(request.current_value)