from enum import Enum


class UserRoleEnum(str, Enum):
    USER = "User"
    ADMIN = "Admin"