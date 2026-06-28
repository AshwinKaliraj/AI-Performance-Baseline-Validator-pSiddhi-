from fastapi import APIRouter
from app.services import user_service

router=APIRouter(
    prefix="/users",
    tags=["User Service"]
)

@router.get("/")
def get_users():
    return user_service.get_all_users()

@router.get("/{user_id}")
def get_user(user_id:int):
    return user_service.get_user_by_id(user_id)