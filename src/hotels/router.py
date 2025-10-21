from datetime import date

from fastapi import APIRouter
from fastapi_cache.decorator import cache

from src.exceptions import HotelsNotFoundException, CurrentHotelNotFoundException
from src.hotels.dao import HotelDAO
from src.hotels.rooms.router import rooms_router
from src.hotels.schemas import SHotels, SCurrentHotel

hotels_router = APIRouter(
    prefix="/hotels",
    tags=["Отели"]
)

hotels_router.include_router(rooms_router)


@hotels_router.get("/{location}")
@cache(expire=30)
async def get_hotels(location: str, date_from: date, date_to: date) -> list[SHotels]:
    hotels = await HotelDAO.find_all(location=location, date_from=date_from, date_to=date_to)

    if not hotels:
        raise HotelsNotFoundException

    return hotels


@hotels_router.get("/id/{hotel_id}")
@cache(expire=30)
async def get_current_hotel(hotel_id: int) -> SCurrentHotel:
    hotel = await HotelDAO.find_by_id(model_id=hotel_id)

    if not hotel:
        raise CurrentHotelNotFoundException

    return hotel
