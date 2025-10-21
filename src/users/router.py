from fastapi import APIRouter, Response
from fastapi.params import Depends

from src.exceptions import UserAlreadyExistException, IncorrectEmailOrPasswordException
from src.users.auth import get_password_hash, authenticate_user, create_access_token
from src.users.dao import UserDAO
from src.users.dependencies import get_current_user
from src.users.models import Users
from src.users.schemas import SUserAuth

users_router = APIRouter(
    prefix="/users",
    tags=["Аутентификация & Пользователи"]
)


@users_router.post("/register")
async def register_user(user_data: SUserAuth):
    existing_user = await UserDAO.find_one_or_none(email=user_data.email)
    if existing_user:
        raise UserAlreadyExistException

    hashed_pass = await get_password_hash(user_data.password)
    await UserDAO.add(email=user_data.email, hashed_password=hashed_pass)


@users_router.post("/login")
async def register_user(response: Response, user_data: SUserAuth):
    existing_user = await authenticate_user(user_data.email, user_data.password)
    if existing_user:
        access_token = await create_access_token({"sub": str(existing_user.id)})
        response.set_cookie(key="access_token", value=access_token, httponly=True)
        return access_token

    raise IncorrectEmailOrPasswordException


@users_router.get("/logout")
async def logout_user(response: Response):
    response.delete_cookie(key="access_token")
    return {"detail": "Вы успешно вышли из системы"}


@users_router.get("/me")
async def read_users_me(current_user: Users = Depends(get_current_user)):
    return current_user
