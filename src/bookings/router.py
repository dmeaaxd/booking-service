from fastapi import APIRouter, Depends

from src.bookings.dao import BookingDAO
from src.bookings.schemas import SBooking
from src.users.dependencies import get_current_user
from src.users.models import Users

bookings_router = APIRouter(
    prefix="/bookings",
    tags=["Бронирование"]
)


@bookings_router.get("")
async def get_bookings(user: Users = Depends(get_current_user)) -> list[SBooking]:
    return await BookingDAO.find_all(user_id=user.id)
