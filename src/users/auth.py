from datetime import datetime, timedelta, UTC

from jose import jwt
from passlib.context import CryptContext
from pydantic import EmailStr

from src.config import settings
from src.users.dao import UserDAO

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


async def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


async def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(days=1)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_SECRET_CODE, algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt


async def authenticate_user(email: EmailStr, password: str):
    existing_user = await UserDAO.find_one_or_none(email=email)
    if existing_user and await verify_password(plain_password=password, hashed_password=existing_user.hashed_password):
        return existing_user

    return None
