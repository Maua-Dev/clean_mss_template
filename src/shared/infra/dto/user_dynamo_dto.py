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

    @staticmethod
    def from_dynamo(user_data: dict) -> "UserDynamoDto":
        """
        Parse data from DynamoDB to UserDynamoDTO
        @param user_data: dict from DynamoDB
        """
        return UserDynamoDto(
            name=user_data["name"],
            email=user_data["email"],
            idUser=int(user_data["idUser"]),
            state=STATE(user_data["state"])
        )

    def to_entity(self) -> User:
        """
        Parse data from UserDynamoDTO to User
        """
        return User(
            name=self.name,
            email=self.email,
            idUser=self.idUser,
            state=self.state
        )

    def __repr__(self):
        return f"UserDynamoDto(name={self.name}, email={self.email}, idUser={self.idUser}, state={self.state})"

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
