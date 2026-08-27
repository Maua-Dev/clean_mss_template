from uuid import UUID

import pytest

from src.modules.user.delete_user.app.delete_user_usecase import DeleteUserUsecase
from src.shared.helpers.errors.usecase_errors import NoUsersFound
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_DeleteUserUsecase:
    def test_delete_user(self):
        user_repo = UserRepositoryMock()
        usecase = DeleteUserUsecase(user_repo)
        user_id = user_repo.users[0].user_id

        deleted = usecase(user_id)

        assert deleted.user_id == user_id
        with pytest.raises(NoUsersFound):
            user_repo.get_user(user_id)

    def test_delete_user_not_found(self):
        user_repo = UserRepositoryMock()
        usecase = DeleteUserUsecase(user_repo)

        with pytest.raises(NoUsersFound):
            usecase(UUID("99999999-9999-4999-8999-999999999999"))
