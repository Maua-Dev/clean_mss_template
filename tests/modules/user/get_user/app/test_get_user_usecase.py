from uuid import UUID

import pytest

from src.modules.user.get_user.app.get_user_usecase import GetUserUsecase
from src.shared.helpers.errors.usecase_errors import NoUsersFound
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_GetUserUsecase:
    def test_get_user(self):
        user_repo = UserRepositoryMock()
        usecase = GetUserUsecase(user_repo)
        user = user_repo.users[0]

        assert usecase(user.user_id) == user

    def test_get_user_not_found(self):
        user_repo = UserRepositoryMock()
        usecase = GetUserUsecase(user_repo)

        with pytest.raises(NoUsersFound):
            usecase(UUID("99999999-9999-4999-8999-999999999999"))
