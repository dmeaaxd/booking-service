from datetime import date

from sqlalchemy import select, and_, func

from src.bookings.models import Bookings
from src.dao.base import BaseDAO
from src.database import async_session_maker
from src.hotels.models import Hotels
from src.hotels.rooms.models import Rooms
from src.hotels.schemas import SHotels


class HotelDAO(BaseDAO):
    model = Hotels

    @classmethod
    async def find_all(cls, location: str, date_from: date, date_to: date):
        async with async_session_maker() as session:
            booked_rooms_subquery = (
                select(
                    func.count(Bookings.id).label('booked_count')
                )
                .select_from(Bookings)
                .join(Rooms, Bookings.room_id == Rooms.id)
                .where(
                    and_(
                        Rooms.hotel_id == Hotels.id,  # корреляция с внешним запросом
                        Bookings.date_from < date_to,
                        Bookings.date_to > date_from
                    )
                )
                .scalar_subquery()
                .correlate(Hotels)
            )

            rooms_left = Hotels.rooms_quantity - func.coalesce(booked_rooms_subquery, 0)

            query = (
                select(
                    Hotels.id,
                    Hotels.name,
                    Hotels.location,
                    Hotels.stars,
                    Hotels.services,
                    Hotels.rooms_quantity,
                    Hotels.image_id,
                    rooms_left.label('rooms_left')
                )
                .where(
                    and_(
                        Hotels.location == location,
                        rooms_left > 0
                    )
                )
            )

            result = await session.execute(query)

            return [
                SHotels.model_validate({
                    "id": row.id,
                    "name": row.name,
                    "location": row.location,
                    "stars": row.stars,
                    "services": row.services,
                    "rooms_quantity": row.rooms_quantity,
                    "image_id": row.image_id,
                    "rooms_left": row.rooms_left
                })
                for row in result
            ]
