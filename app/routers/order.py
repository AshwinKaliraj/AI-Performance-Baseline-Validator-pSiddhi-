from fastapi import APIRouter
from app.services import order_service

router=APIRouter(
    prefix="/orders",
    tags=["Order Service"]
)

@router.get("/")
def get_orders():
    return order_service.get_all_orders()

@router.get("/{order_id}")
def get_order(order_id:int):
    return order_service.get_order_by_id(order_id)