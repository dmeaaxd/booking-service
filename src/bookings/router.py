from fastapi import APIRouter
from sqlalchemy import select

from src.bookings.models import Bookings
from src.database import async_session_maker

bookings_router = APIRouter(
    prefix="/bookings",
    tags=["Бронирование"]
)


@bookings_router.get("")
async def ger_bookings():
    async with async_session_maker() as session:
        query = select(Bookings)
        bookings = await session.execute(query)
        return bookings.mappings().all()

@bookings_router.get("{booking_id}")
def ger_booking(booking_id: int):
    ...


