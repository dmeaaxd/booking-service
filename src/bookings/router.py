from datetime import date

from fastapi import APIRouter, Depends

from src.bookings.dao import BookingDAO
from src.bookings.schemas import SBooking
from src.exceptions import RoomsNotFoundException
from src.users.dependencies import get_current_user
from src.users.models import Users

bookings_router = APIRouter(
    prefix="/bookings",
    tags=["Бронирование"]
)


@bookings_router.get("")
async def get_bookings(user: Users = Depends(get_current_user)) -> list[SBooking]:
    return await BookingDAO.find_all(user_id=user.id)


@bookings_router.post("")
async def add_booking(room_id: int, date_from: date, date_to: date, user: Users = Depends(get_current_user)):
    booking = await BookingDAO.add(user_id = user.id, room_id=room_id, date_from=date_from, date_to=date_to)

    if not booking:
        raise RoomsNotFoundException

    return booking