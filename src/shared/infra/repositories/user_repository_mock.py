from typing import List

from src.shared.domain.entities.user import User
from src.shared.domain.enums.state_enum import STATE
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.usecase_errors import NoItemsFound


class UserRepositoryMock(IUserRepository):
    users: List[User]
    user_counter: int

    def __init__(self):
        self.users = [
            User(name="Bruno Soller", email="soller@soller.com", idUser=1, state=STATE.APPROVED),
            User(name="Vitor Brancas", email="brancas@brancas.com", idUser=2, state=STATE.REJECTED),
            User(name="João Vilas", email="bruno@bruno.com", idUser=3, state=STATE.PENDING)
        ]
        self.user_counter = 3

    def get_user(self, idUser: int) -> User:
        for user in self.users:
            if user.idUser == idUser:
                return user
        raise NoItemsFound("idUser")

    def get_all_user(self) -> List[User]:
        return self.users

    def create_user(self, new_user: User) -> User:
        self.users.append(new_user)
        self.user_counter += 1
        return new_user

    def delete_user(self, idUser: int) -> User:
        for idx, user in enumerate(self.users):
            if user.idUser == idUser:
                return self.users.pop(idx)

        raise NoItemsFound("idUser")

    def update_user(self, idUser: int, new_name: str) -> User:
        for user in self.users:
            if user.idUser == idUser:
                user.name = new_name
                return user

        raise NoItemsFound("idUser")

    def get_user_counter(self) -> int:
        return self.user_counter
