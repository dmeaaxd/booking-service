from src.dao.base import BaseDAO
from src.hotels.rooms.models import Rooms


class RoomDAO(BaseDAO):
    model = Rooms