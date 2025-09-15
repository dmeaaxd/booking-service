from src.dao.base import BaseDAO
from src.users.models import Users


class UserDAO(BaseDAO):
    model = Users
