from typing import List

from src.shared.domain.entities.user import User
from src.shared.domain.repositories.user_repository_interface import IUserRepository


class UserRepositoryDynamo(IUserRepository):
    def get_user(self, idUser: int) -> User:
        pass

    def get_all_user(self) -> List[User]:
        pass

    def create_user(self, new_user: User) -> User:
        pass

    def delete_user(self, idUser: int) -> User:
        pass

    def update_user(self, idUser: int, new_name: str) -> User:
        pass

    def get_user_counter(self) -> int:
        pass
