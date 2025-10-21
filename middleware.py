from fastapi.middleware.cors import CORSMiddleware

from src.main import app

origins = [
    "http://localhost:8081"
]


middleware = CORSMiddleware(
    app=app,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Origin", "Access-Control-Allow-Headers",
                   "Authorization"],
)
