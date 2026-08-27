from abc import ABC, abstractmethod
from typing import List
from uuid import UUID
from pydantic import EmailStr

from src.shared.domain.entities.user import User

class IUserRepository(ABC):

    @abstractmethod
    def get_user(self, user_id: UUID) -> User:
        """Retrieve a user by their unique identifier.

        Args:
            user_id: UUID of the user to retrieve.

        Returns:
            The user associated with the given UUID.

        Raises:
            NoUsersFound: If no user exists with the given UUID.
        """
        pass

    @abstractmethod
    def get_user_by_email(self, user_email: EmailStr) -> User:
        """Retrieve a user by their email.

        Args:
            user_email: Email of the user to retrieve.

        Returns:
            The user associated with the given email.

        Raises:
            NoUsersFound: If no user exists with the given email.
        """
        pass

    @abstractmethod
    def get_all_users(self) -> List[User]:
        """Retrieve all stored users.

        Returns:
            A list containing all users. The list is empty when no users exist.
        """
        pass

    @abstractmethod
    def create_user(self, new_user: User) -> User:
        """Persist a new user.

        Args:
            new_user: User to persist.

        Returns:
            The persisted user.

        Raises:
            DuplicatedUser: If a user with the same identifier already exists.
        """
        pass

    @abstractmethod
    def delete_user(self, user_id: UUID) -> User:
        """Delete a user by their unique identifier.

        Args:
            user_id: UUID of the user to delete.

        Returns:
            The deleted user.

        Raises:
            NoUsersFound: If no user exists with the given UUID.
        """
        pass

    @abstractmethod
    def update_user(self, updated_user: User) -> User:
        """Replace the stored data for an existing user.

        Args:
            updated_user: User containing the identifier and updated data.

        Returns:
            The updated user.

        Raises:
            NoUsersFound: If the user to update does not exist.
        """
        pass

    @abstractmethod
    def reallocate_user(self, updated_user: User) -> User:
        """Replace the user matched by email with authorizer data (may change user_id).

        Looks up by ``updated_user.user_email``, then substitutes stored fields
        with the given user. When ``user_id`` changes, the old partition key is
        removed and the new one is written.

        Args:
            updated_user: User built from MSS authorizer claims (id, name, email)
                plus preserved domain fields (role, created_at).

        Returns:
            The substituted user.

        Raises:
            NoUsersFound: If no user exists with the given email.
            DuplicatedUser: If the new user_id already belongs to another user.
        """
        pass

    @abstractmethod
    def get_user_counter(self) -> int:
        """Return the total number of users ever created.

        Returns:
            The cumulative number of created users.
        """
        pass
   
    
    