from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.bookings.router import bookings_router
from src.hotels.rooms.router import rooms_router
from src.hotels.router import hotels_router
from src.redis_db import lifespan
from src.users.router import users_router

app = FastAPI(lifespan=lifespan)

app.include_router(users_router)
app.include_router(bookings_router)
app.include_router(hotels_router)   # содержит в себе роутер rooms
