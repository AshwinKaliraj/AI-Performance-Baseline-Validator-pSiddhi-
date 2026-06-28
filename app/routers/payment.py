from fastapi import APIRouter
from app.services import payment_service

router=APIRouter(
    prefix="/payments",
    tags=["Payment Service"]
)

@router.get("/")
def get_payments():
    return payment_service.get_all_payments()

@router.get("/{payment_id}")
def get_payment(payment_id:int):
    return payment_service.get_payment_by_id(payment_id)