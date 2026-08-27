from uuid import UUID

import pytest

from src.modules.user.auth_user.app.auth_user_usecase import AuthUserUsecase
from src.shared.domain.enums.user_role_enum import UserRoleEnum
from src.shared.helpers.errors.usecase_errors import NoUsersFound
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_AuthUserUsecase:
    def test_auth_user_creates_when_email_missing(self):
        user_repo = UserRepositoryMock()
        usecase = AuthUserUsecase(user_repo)
        user_id = UUID("dddddddd-dddd-4ddd-8ddd-dddddddddddd")

        user, case_number = usecase(
            user_id=user_id,
            user_name="Dave",
            user_email="dave@example.com",
        )

        assert case_number == 1
        assert user.user_id == user_id
        assert user.user_name == "Dave"
        assert user.user_email == "dave@example.com"
        assert user.user_role == UserRoleEnum.USER
        assert user_repo.users[-1] == user

    def test_auth_user_reallocates_id_and_name_when_email_exists(self):
        user_repo = UserRepositoryMock()
        usecase = AuthUserUsecase(user_repo)
        existing = user_repo.users[1]
        old_id = existing.user_id
        new_id = UUID("eeeeeeee-eeee-4eee-8eee-eeeeeeeeeeee")

        user, case_number = usecase(
            user_id=new_id,
            user_name="Bob Updated",
            user_email=str(existing.user_email),
        )

        assert case_number == 0
        assert user.user_id == new_id
        assert user.user_name == "Bob Updated"
        assert user.user_email == existing.user_email
        assert user.user_role == existing.user_role
        assert user.created_at == existing.created_at
        assert user_repo.get_user(new_id) == user
        with pytest.raises(NoUsersFound):
            user_repo.get_user(old_id)

    def test_auth_user_updates_name_when_same_id(self):
        user_repo = UserRepositoryMock()
        usecase = AuthUserUsecase(user_repo)
        existing = user_repo.users[1]

        user, case_number = usecase(
            user_id=existing.user_id,
            user_name="Bobby",
            user_email=str(existing.user_email),
        )

        assert case_number == 0
        assert user.user_id == existing.user_id
        assert user.user_name == "Bobby"
        assert user.user_role == existing.user_role
