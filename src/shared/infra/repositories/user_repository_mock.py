from typing import List
from uuid import UUID

from pydantic import EmailStr

from src.shared.domain.entities.user import User
from src.shared.domain.enums.user_role_enum import UserRoleEnum
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.usecase_errors import DuplicatedUser, NoUsersFound


class UserRepositoryMock(IUserRepository):
    users: List[User]
    user_counter: int

    def __init__(self):
        self.users = [
            User(
                user_id=UUID("aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa"),
                user_name="Alice Admin",
                user_email="alice@example.com",
                user_role=UserRoleEnum.ADMIN,
                created_at=1_700_000_000,
            ),
            User(
                user_id=UUID("bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb"),
                user_name="Bob User",
                user_email="bob@example.com",
                user_role=UserRoleEnum.USER,
                created_at=1_700_000_100,
            ),
            User(
                user_id=UUID("cccccccc-cccc-4ccc-8ccc-cccccccccccc"),
                user_name="Carol User",
                user_email="carol@example.com",
                user_role=UserRoleEnum.USER,
                created_at=1_700_000_200,
            ),
        ]
        self.user_counter = len(self.users)

    def get_user(self, user_id: UUID) -> User:
        for user in self.users:
            if user.user_id == user_id:
                return user
        raise NoUsersFound("user_id")

    def get_user_by_email(self, user_email: EmailStr) -> User:
        email = str(user_email).lower()
        for user in self.users:
            if str(user.user_email).lower() == email:
                return user
        raise NoUsersFound("user_email")

    def get_all_users(self) -> List[User]:
        return self.users

    def create_user(self, new_user: User) -> User:
        for user in self.users:
            if user.user_id == new_user.user_id:
                raise DuplicatedUser("user_id")
            if str(user.user_email).lower() == str(new_user.user_email).lower():
                raise DuplicatedUser("user_email")

        self.users.append(new_user)
        self.user_counter += 1
        return new_user

    def delete_user(self, user_id: UUID) -> User:
        for idx, user in enumerate(self.users):
            if user.user_id == user_id:
                return self.users.pop(idx)

        raise NoUsersFound("user_id")

    def update_user(self, updated_user: User) -> User:
        for idx, user in enumerate(self.users):
            if user.user_id == updated_user.user_id:
                self.users[idx] = updated_user
                return updated_user

        raise NoUsersFound("user_id")

    def reallocate_user(self, updated_user: User) -> User:
        email = str(updated_user.user_email).lower()
        matched_idx = None
        for idx, user in enumerate(self.users):
            if str(user.user_email).lower() == email:
                matched_idx = idx
                break

        if matched_idx is None:
            raise NoUsersFound("user_email")

        for idx, user in enumerate(self.users):
            if user.user_id == updated_user.user_id and idx != matched_idx:
                raise DuplicatedUser("user_id")

        self.users[matched_idx] = updated_user
        return updated_user

    def get_user_counter(self) -> int:
        return self.user_counter
