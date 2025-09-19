from datetime import datetime, UTC

from fastapi import Request, Depends
from jose import jwt, JWTError

from src.config import settings
from src.exceptions import JWTExpiredException, JWTNotFoundException, JWTIncorrectFormatException, \
    UserIsNotPresentException
from src.users.dao import UserDAO


async def get_token(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise JWTNotFoundException
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(
            token=token, key=settings.JWT_SECRET_CODE, algorithms=settings.JWT_ALGORITHM
        )
    except JWTError:
        raise JWTIncorrectFormatException

    expire: str = payload.get("exp")
    if (not expire) or (int(expire) < datetime.now(UTC).timestamp()):
        raise JWTExpiredException

    user_id: str = payload.get("sub")
    if not user_id:
        raise UserIsNotPresentException

    user = await UserDAO.find_by_id(int(user_id))
    if not user:
        raise UserIsNotPresentException

    return user
