from datetime import date

from sqlalchemy import select, and_, or_, func, not_, exists

from src.bookings.models import Bookings
from src.dao.base import BaseDAO
from src.database import async_session_maker
from src.hotels.models import Hotels
from src.hotels.rooms.models import Rooms


class HotelDAO(BaseDAO):
    model = Hotels

    @classmethod
    async def find_all(cls, location: str, date_from: date, date_to: date):
        async with async_session_maker() as session:
            # Подзапрос для подсчета забронированных номеров для каждого отеля
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

            query = (
                select(Hotels)
                .where(
                    and_(
                        Hotels.location == location,
                        Hotels.rooms_quantity > func.coalesce(booked_rooms_subquery, 0)
                    )
                )
            )

            result = await session.execute(query)
            return result.scalars().all()