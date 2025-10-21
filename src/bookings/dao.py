from datetime import date

from sqlalchemy import select, and_, or_, func, insert

from src.bookings.models import Bookings
from src.bookings.schemas import SBooking
from src.dao.base import BaseDAO
from src.database import async_session_maker
from src.hotels.rooms.models import Rooms


class BookingDAO(BaseDAO):
    model = Bookings

    @classmethod
    async def find_all(cls, user_id: int):
        async with async_session_maker() as session:
            bookings = select(
                Bookings.id,
                Bookings.room_id,
                Bookings.user_id,
                Bookings.date_from,
                Bookings.date_to,
                Bookings.price,
                Bookings.total_cost,
                Bookings.total_days,
                Rooms.image_id,
                Rooms.name,
                Rooms.description,
                Rooms.services
            ).select_from(Bookings).join(
                Rooms, Bookings.room_id == Rooms.id
            ).where(
                Bookings.user_id == user_id
            )

            result = await session.execute(bookings)

            return [
                SBooking.model_validate({
                    "id": row.id,
                    "room_id": row.room_id,
                    "user_id": row.user_id,
                    "date_from": row.date_from,
                    "date_to": row.date_to,
                    "price": row.price,
                    "total_cost": row.total_cost,
                    "total_days": row.total_days,
                    "room_image_id": row.image_id,
                    "room_name": row.name,
                    "room_description": row.description,
                    "room_services": row.services
                })
                for row in result
            ]

    @classmethod
    async def add(cls, user_id: int, room_id: int, date_from: date, date_to: date):
        async with async_session_maker() as session:
            booked_rooms = select(Bookings).where(
                and_(
                    Bookings.room_id == room_id,
                    or_(
                        and_(
                            Bookings.date_from >= date_from,
                            Bookings.date_from <= date_to,
                        ),
                        and_(
                            Bookings.date_from <= date_from,
                            Bookings.date_to > date_from,
                        )
                    )
                )
            ).cte("booked_rooms")

            get_rooms_left = select(
                Rooms.quantity - func.count(booked_rooms.c.room_id).label("rooms_left")
            ).select_from(Rooms).outerjoin(
                booked_rooms, booked_rooms.c.room_id == Rooms.id
            ).where(Rooms.id == room_id).group_by(
                Rooms.quantity, booked_rooms.c.room_id
            )

            rooms_left = await session.execute(get_rooms_left)
            rooms_left: int = rooms_left.scalar()

            # print(rooms_left)

            if rooms_left > 0:
                get_price = select(Rooms.price).filter_by(id=room_id)
                price = await session.execute(get_price)
                price: int = price.scalar()
                add_bookings = insert(Bookings).values(
                    room_id=room_id,
                    user_id=user_id,
                    date_from=date_from,
                    date_to=date_to,
                    price=price
                ).returning(Bookings)

                new_booking = await session.execute(add_bookings)
                await session.commit()

                return new_booking.scalar()
            else:
                return None


