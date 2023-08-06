from enum import Enum, IntEnum


class Gender(str, Enum):
    Male = "Male"
    Female = "Female"


class StateEnum(str, Enum):
    """
    允许登录的权限,1:允许,2:禁用
    """
    allow = "allow"
    forbidden = "forbidden"
