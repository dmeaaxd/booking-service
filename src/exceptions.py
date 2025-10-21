from fastapi import HTTPException, status


class BaseHTTPException(HTTPException):
    status_code = 500
    detail = "Internal Server Error"

    def __init__(self, ):
        super().__init__(self.status_code, self.detail)


class UsersException(BaseHTTPException):
    pass


class JWTException(BaseHTTPException):
    pass


class RoomsException(BaseHTTPException):
    pass


class HotelsException(BaseHTTPException):
    pass


class BookingsException(BaseHTTPException):
    pass


# Users
class UserAlreadyExistException(UsersException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Пользователь уже существует"


class IncorrectEmailOrPasswordException(UsersException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверная почта или пароль"


class UserIsNotPresentException(UsersException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Ошибка содержания токена"


# JWT
class JWTExpiredException(JWTException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Токен истек"


class JWTNotFoundException(JWTException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Вы не вошли в систему"


class JWTIncorrectFormatException(JWTException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверный формат токена"


# Rooms
class RoomsNotFoundException(JWTException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Не осталось свободных номеров"


# Hotels
class HotelsNotFoundException(HotelsException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Не осталось свободных отелей"


# Bookings
class BookingsDeleteException(BookingsException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Невозможно произвести удаление"