from abc import ABC, abstractmethod
from typing import List

from src.shared.domain.entities.user import User


class IUserRepository(ABC):

    @abstractmethod
    def get_user(self, idUser: int) -> User:
        """
        If user not found raise NoItemsFound
        """
        pass

    @abstractmethod
    def get_all_user(self) -> List[User]:
        pass
    @abstractmethod
    def create_user(self, new_user: User) -> User:
        pass
