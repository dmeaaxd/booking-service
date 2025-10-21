from sqlalchemy import select, insert, delete, update

from src.database import async_session_maker


class BaseDAO:
    model = None

    @classmethod
    async def find_all(cls, **filters):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filters)
            result = await session.execute(query)
            return result.mappings().all()

    @classmethod
    async def find_one_or_none(cls, **filters):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filters)
            result = await session.execute(query)
            return result.mappings().one_or_none()

    @classmethod
    async def find_by_id(cls, model_id):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(id=model_id)
            result = await session.execute(query)
            return result.mappings().one_or_none()

    @classmethod
    async def add(cls, **data):
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def delete(cls, **data):
        async with async_session_maker() as session:
            query = delete(cls.model).filter_by(**data)
            result = await session.execute(query)
            await session.commit()
            return result   # для проверки удалилось ли что-то

    @classmethod
    async def update(cls, **data):
        async with async_session_maker() as session:
            query = update(cls.model).filter_by(**data)
            await session.execute(query)
            await session.commit()