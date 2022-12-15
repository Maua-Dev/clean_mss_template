import abc
import re

from src.shared.domain.enums.state_enum import STATE
from src.shared.helpers.errors.domain_errors import EntityError


class User(abc.ABC):
    name: str
    email: str
    state: STATE
    MIN_NAME_LENGTH = 2
    idUser: int

    def __init__(self, name: str, email: str, state: STATE, idUser: int = None):
        if not User.validate_name(name):
            raise EntityError("name")
        self.name = name

        if not User.validate_email(email):
            raise EntityError("email")
        self.email = email

        if type(idUser) == int:
            if idUser < 0:
                raise EntityError("idUser")

        if type(idUser) != int and idUser is not None:
            raise EntityError("idUser")

        self.idUser = idUser

        if type(state) != STATE:
            raise EntityError("state")
        self.state = state

    @staticmethod
    def validate_name(name: str) -> bool:
        if name is None:
            return False
        elif type(name) != str:
            return False
        elif len(name) < User.MIN_NAME_LENGTH:
            return False

        return True

    @staticmethod
    def validate_email(email: str) -> bool:
        if email is None:
            return False

        regex = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

        return bool(re.fullmatch(regex, email))



    def __repr__(self):
        return f"User(name={self.name}, email={self.email}, idUser={self.idUser}, state={self.state})"
