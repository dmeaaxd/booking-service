from datetime import date

from fastapi import APIRouter

from src.exceptions import HotelsNotFoundException
from src.hotels.dao import HotelDAO
from src.hotels.rooms.router import rooms_router
from src.hotels.schemas import SHotels

hotels_router = APIRouter(
    prefix="/hotels",
    tags=["Отели"]
)

hotels_router.include_router(rooms_router)


@hotels_router.get("/{location}")
async def get_hotels(location: str, date_from: date, date_to: date) -> list[SHotels]:
    hotels = await HotelDAO.find_all(location=location, date_from=date_from, date_to=date_to)

    if not hotels:
        raise HotelsNotFoundException

    return hotels