from datetime import date
from time import sleep

from fastapi import APIRouter
from fastapi_cache.decorator import cache

from src.exceptions import RoomsNotFoundException
from src.hotels.rooms.dao import RoomDAO
from src.hotels.rooms.schemas import SRooms

rooms_router = APIRouter(
    prefix="/rooms",
    tags=["Номера"]
)

@rooms_router.get("/{hotel_id}")
@cache(expire=60)
async def get_rooms(hotel_id: int, date_from: date, date_to: date) -> list[SRooms]:
    sleep(3)
    rooms = await RoomDAO.find_all(hotel_id=hotel_id, date_from=date_from, date_to=date_to)

    if not rooms:
        raise RoomsNotFoundException

    return rooms
