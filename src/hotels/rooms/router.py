from fastapi import APIRouter

rooms_router = APIRouter(
    prefix="/rooms",
    tags=["Номера"]
)

