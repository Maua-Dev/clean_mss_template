from decimal import Decimal

from src.shared.domain.entities.user import User
from src.shared.domain.enums.state_enum import STATE


class UserDynamoDTO:
    name: str
    email: str
    state: STATE
    user_id: int

    def __init__(self, name: str, email: str, state: STATE, user_id: int):
        self.name = name
        self.email = email
        self.user_id = user_id
        self.state = state

    @staticmethod
    def from_entity(user: User) -> "UserDynamoDTO":
        """
        Parse data from User to UserDynamoDTO
        """
        return UserDynamoDTO(
            name=user.name,
            email=user.email,
            user_id=user.user_id,
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
            "user_id": Decimal(self.user_id),
            "state": self.state.value
        }

    @staticmethod
    def from_dynamo(user_data: dict) -> "UserDynamoDTO":
        """
        Parse data from DynamoDB to UserDynamoDTO
        @param user_data: dict from DynamoDB
        """
        return UserDynamoDTO(
            name=user_data["name"],
            email=user_data["email"],
            user_id=int(user_data["user_id"]),
            state=STATE(user_data["state"])
        )

    def to_entity(self) -> User:
        """
        Parse data from UserDynamoDTO to User
        """
        return User(
            name=self.name,
            email=self.email,
            user_id=self.user_id,
            state=self.state
        )

    def __repr__(self):
        return f"UserDynamoDto(name={self.name}, email={self.email}, user_id={self.user_id}, state={self.state})"

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
