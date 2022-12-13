from abc import ABC, abstractmethod

from src.shared.domain.entities.user import User


class IUserRepository(ABC):

    @abstractmethod
    def get_user(self, idUser: int) -> User:
        """
        If user not found raise NoItemsFound
        """
        pass
