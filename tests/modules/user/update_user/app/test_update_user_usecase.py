from uuid import UUID

import pytest

from src.modules.user.update_user.app.update_user_usecase import UpdateUserUsecase
from src.shared.helpers.errors.usecase_errors import NoUsersFound
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_UpdateUserUsecase:
    def test_update_user(self):
        user_repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(user_repo)
        user = user_repo.users[0]

        updated = usecase(
            user_id=user.user_id,
            user_name="Alice Updated",
            user_email="alice.updated@example.com",
            user_role="Admin",
        )

        assert updated.user_name == "Alice Updated"
        assert updated.created_at == user.created_at

    def test_update_user_not_found(self):
        user_repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(user_repo)

        with pytest.raises(NoUsersFound):
            usecase(
                user_id=UUID("99999999-9999-4999-8999-999999999999"),
                user_name="Ghost",
                user_email="ghost@example.com",
                user_role="User",
            )
