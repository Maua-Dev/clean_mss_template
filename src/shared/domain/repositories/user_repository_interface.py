from abc import ABC, abstractmethod
from typing import List

from src.shared.domain.entities.user import User


class IUserRepository(ABC):

    @abstractmethod
    def get_user(self, user_id: int) -> User:
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

    @abstractmethod
    def delete_user(self, user_id: int) -> User:
        """
        If user not found raise NoItemsFound
        """
        pass

    @abstractmethod
    def update_user(self, user_id: int, new_name: str) -> User:
        """
        If user not found raise NoItemsFound
        """
        pass

    @abstractmethod
    def get_user_counter(self) -> int:
        """
        Returns the number of all users that have ever been created
        """
        pass
