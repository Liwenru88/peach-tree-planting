from beanie import Indexed

from app.models.base_model import BaseDocument
from app.utils.enumerate import Gender, StateEnum


class User(BaseDocument):
    __doc__ = "用户表"

    account: Indexed(str, unique=True)
    mobile: Indexed(str, unique=True)
    username: Indexed(str)
    email: Indexed(str)
    address: str
    gender: Gender
    state: StateEnum = StateEnum.allow
    password: str

    class Settings:
        name = "users"
        use_state_management = True
