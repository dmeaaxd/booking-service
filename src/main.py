from fastapi import FastAPI
from src.bookings.router import bookings_router

app = FastAPI()
app.include_router(bookings_router)