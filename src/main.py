from fastapi import FastAPI
from src.bookings.router import bookings_router
from src.users.router import users_router

app = FastAPI()
app.include_router(users_router)
app.include_router(bookings_router)