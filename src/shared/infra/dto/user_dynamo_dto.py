from decimal import Decimal

from src.shared.domain.entities.user import User
from src.shared.domain.enums.state_enum import STATE


class UserDynamoDto:
    name: str
    email: str
    state: STATE
    idUser: int

    def __init__(self, name: str, email: str, state: STATE, idUser: int):
        self.name = name
        self.email = email
        self.idUser = idUser
        self.state = state

    @staticmethod
    def from_entity(user: User) -> "UserDynamoDto":
        """
        Parse data from User to UserDynamoDTO
        """
        return UserDynamoDto(
            name=user.name,
            email=user.email,
            idUser=user.idUser,
            state=user.state
        )

    def to_dynamo(self) -> dict:
        """
        Parse data from UserDynamoDTO to dict
        """
        return {
            "entity": "user",
            "name": self.name,
            "email": self.email,
            "idUser": Decimal(self.idUser),
            "state": self.state.value
        }

    def __repr__(self):
        return f"UserDynamoDto(name={self.name}, email={self.email}, idUser={self.idUser}, state={self.state})"

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
