from datetime import date

from fastapi import APIRouter

from src.exceptions import HotelsNotFoundException
from src.hotels.dao import HotelDAO

hotels_router = APIRouter(
    prefix="/hotels",
    tags=["Отели"]
)


@hotels_router.get("/{location}")
async def get_hotels(location: str, date_from: date, date_to: date):
    hotels = await HotelDAO.find_all(location=location, date_from=date_from, date_to=date_to)
    if not hotels:
        raise HotelsNotFoundException
    return hotels