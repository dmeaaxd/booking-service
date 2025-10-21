from datetime import date

from fastapi import APIRouter, Depends, Response, status
from fastapi_cache.decorator import cache

from src.bookings.dao import BookingDAO
from src.bookings.schemas import SBooking
from src.exceptions import RoomsNotFoundException, BookingsDeleteException
from src.users.dependencies import get_current_user
from src.users.models import Users

bookings_router = APIRouter(
    prefix="/bookings",
    tags=["Бронирование"]
)


@bookings_router.get("")
@cache(expire=5)
async def get_bookings(user: Users = Depends(get_current_user)) -> list[SBooking]:
    return await BookingDAO.find_all(user_id=user.id)


@bookings_router.post("")
async def add_booking(room_id: int, date_from: date, date_to: date, user: Users = Depends(get_current_user)):
    booking = await BookingDAO.add(user_id=user.id, room_id=room_id, date_from=date_from, date_to=date_to)

    if not booking:
        raise RoomsNotFoundException

    return booking


@bookings_router.delete("/{booking_id}")
async def delete_booking(booking_id: int, user: Users = Depends(get_current_user)):
    query = await BookingDAO.delete(id=booking_id, user_id=user.id)

    if query.rowcount == 0:
        raise BookingsDeleteException

    return Response(status_code=status.HTTP_204_NO_CONTENT)
