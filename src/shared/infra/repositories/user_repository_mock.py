from typing import List

from src.shared.domain.entities.user import User
from src.shared.domain.enums.state_enum import STATE
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.usecase_errors import NoItemsFound


class UserRepositoryMock(IUserRepository):
    users: List[User]

    def __init__(self):
        self.users = [
            User(name="Bruno Soller", email="soller@soller.com", idUser=1, state=STATE.APPROVED),
            User(name="Vitor Brancas", email="brancas@brancas.com", idUser=2, state=STATE.REJECTED),
            User(name="João Vilas", email="bruno@bruno.com", idUser=3, state=STATE.PENDING)
        ]

    def get_user(self, idUser: int) -> User:
        for user in self.users:
            if user.idUser == idUser:
                return user
        raise NoItemsFound("idUser")
