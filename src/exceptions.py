from fastapi import HTTPException, status

UserAlreadyExistException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Пользователь уже существует",
)

IncorrectEmailOrPasswordException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Неверная почта или пароль"
)

JWTExpiredException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Токен истек"
)

JWTNotFoundException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Вы не вошли в систему"
)

JWTIncorrectFormatException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Неверный формат токена"
)

UserIsNotPresentException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Ошибка содержания токена"
)

RoomCanNotBeBookedException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Не осталось свободных номеров"
)


