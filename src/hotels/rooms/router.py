from datetime import date

from fastapi import APIRouter

from src.exceptions import RoomsNotFoundException
from src.hotels.rooms.dao import RoomDAO
from src.hotels.rooms.schemas import SRooms

rooms_router = APIRouter(
    prefix="/rooms",
    tags=["Номера"]
)

@rooms_router.get("/{hotel_id}")
async def get_rooms(hotel_id: int, date_from: date, date_to: date) -> list[SRooms]:
    rooms = await RoomDAO.find_all(hotel_id=hotel_id, date_from=date_from, date_to=date_to)

    if not rooms:
        raise RoomsNotFoundException

    return rooms