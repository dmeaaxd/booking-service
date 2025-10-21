from datetime import date

from sqlalchemy import select, and_, func

from src.bookings.models import Bookings
from src.dao.base import BaseDAO
from src.database import async_session_maker
from src.hotels.rooms.models import Rooms
from src.hotels.rooms.schemas import SRooms


class RoomDAO(BaseDAO):
    model = Rooms

    @classmethod
    async def find_all(cls, hotel_id: int, date_from: date, date_to: date):
        async with async_session_maker() as session:
            booked_rooms_subquery = (
                select(
                    func.count(Bookings.id).label('booked_count')
                )
                .select_from(Bookings)
                .where(
                    and_(
                        Bookings.room_id == Rooms.id,  # корреляция с внешним запросом
                        Bookings.date_from < date_to,
                        Bookings.date_to > date_from
                    )
                )
                .scalar_subquery()
                .correlate(Rooms)
            )

            # Вычисляем количество оставшихся комнат
            rooms_left = Rooms.quantity - func.coalesce(booked_rooms_subquery, 0)

            query = (
                select(
                    Rooms.id,
                    Rooms.hotel_id,
                    Rooms.name,
                    Rooms.description,
                    Rooms.price,
                    Rooms.services,
                    Rooms.quantity,
                    Rooms.image_id,
                    rooms_left.label('rooms_left')
                )
                .where(
                    and_(
                        Rooms.hotel_id == hotel_id,
                        rooms_left > 0
                    )
                )
            )

            result = await session.execute(query)

            return [
                SRooms(
                    id=row.id,
                    hotel_id=row.hotel_id,
                    name=row.name,
                    description=row.description or "",
                    price=row.price,
                    services=row.services or {},
                    quantity=row.quantity,
                    image_id=row.image_id,
                    rooms_left=row.rooms_left
                )
                for row in result
            ]
