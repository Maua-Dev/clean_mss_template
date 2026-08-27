from uuid import UUID

import pytest

from src.shared.domain.entities.user import User
from src.shared.domain.enums.user_role_enum import UserRoleEnum
from src.shared.helpers.errors.usecase_errors import DuplicatedUser, NoUsersFound
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_UserRepositoryMock:
    def test_get_user(self):
        repo = UserRepositoryMock()
        user = repo.get_user(UUID("aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa"))
        assert user.user_name == "Alice Admin"

    def test_get_user_by_email(self):
        repo = UserRepositoryMock()
        user = repo.get_user_by_email("bob@example.com")
        assert user.user_name == "Bob User"

    def test_get_user_by_email_not_found(self):
        repo = UserRepositoryMock()
        with pytest.raises(NoUsersFound):
            repo.get_user_by_email("nobody@example.com")

    def test_get_all_users(self):
        repo = UserRepositoryMock()
        assert len(repo.get_all_users()) == 3

    def test_create_user(self):
        repo = UserRepositoryMock()
        user = User(
            user_name="Dave",
            user_email="dave@example.com",
            user_role=UserRoleEnum.USER,
        )
        created = repo.create_user(user)
        assert created == user
        assert repo.get_user_counter() == 4

    def test_create_user_duplicated_email(self):
        repo = UserRepositoryMock()
        with pytest.raises(DuplicatedUser):
            repo.create_user(User(
                user_name="Clone",
                user_email="alice@example.com",
            ))

    def test_delete_user(self):
        repo = UserRepositoryMock()
        user_id = repo.users[0].user_id
        deleted = repo.delete_user(user_id)
        assert deleted.user_id == user_id
        with pytest.raises(NoUsersFound):
            repo.get_user(user_id)

    def test_update_user(self):
        repo = UserRepositoryMock()
        existing = repo.users[0]
        updated = User(
            user_id=existing.user_id,
            user_name="Alice Updated",
            user_email="alice.updated@example.com",
            user_role=UserRoleEnum.ADMIN,
            created_at=existing.created_at,
        )
        result = repo.update_user(updated)
        assert result.user_name == "Alice Updated"

    def test_reallocate_user_changes_id(self):
        repo = UserRepositoryMock()
        existing = repo.users[1]
        new_id = UUID("eeeeeeee-eeee-4eee-8eee-eeeeeeeeeeee")
        substituted = User(
            user_id=new_id,
            user_name="Bob From Graph",
            user_email=existing.user_email,
            user_role=existing.user_role,
            created_at=existing.created_at,
        )

        result = repo.reallocate_user(substituted)

        assert result.user_id == new_id
        assert repo.get_user(new_id).user_name == "Bob From Graph"
        with pytest.raises(NoUsersFound):
            repo.get_user(existing.user_id)

    def test_get_user_counter(self):
        repo = UserRepositoryMock()
        assert repo.get_user_counter() == 3
