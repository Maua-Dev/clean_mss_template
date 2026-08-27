from uuid import UUID

import pytest

from src.modules.user.create_user.app.create_user_usecase import CreateUserUsecase
from src.shared.domain.enums.user_role_enum import UserRoleEnum
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_CreateUserUsecase:
    def test_create_user(self):
        user_repo = UserRepositoryMock()
        usecase = CreateUserUsecase(user_repo)
        user_id = UUID("aaaaaaaa-bbbb-4ccc-8ddd-eeeeeeeeeeee")

        user = usecase(
            user_id=user_id,
            user_name="Dave",
            user_email="dave@example.com",
        )

        assert user_repo.users[-1] == user
        assert user.user_id == user_id
        assert user.user_name == "Dave"
        assert user.user_role == UserRoleEnum.USER

    def test_create_user_invalid_email(self):
        user_repo = UserRepositoryMock()
        usecase = CreateUserUsecase(user_repo)

        with pytest.raises(EntityError):
            usecase(
                user_id=UUID("aaaaaaaa-bbbb-4ccc-8ddd-eeeeeeeeeeee"),
                user_name="Dave",
                user_email="not-an-email",
            )
