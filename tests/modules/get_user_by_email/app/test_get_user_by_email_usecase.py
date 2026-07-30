import pytest

from src.modules.get_user_by_email.app.get_user_by_email_usecase import GetUserByEmailUsecase
from src.shared.helpers.errors.usecase_errors import NoUsersFound
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_GetUserByEmailUsecase:
    def test_get_user_by_email(self):
        repo = UserRepositoryMock()
        usecase = GetUserByEmailUsecase(repo)

        user = usecase("alice@example.com")

        assert user.user_name == "Alice Admin"

    def test_get_user_by_email_not_found(self):
        repo = UserRepositoryMock()
        usecase = GetUserByEmailUsecase(repo)

        with pytest.raises(NoUsersFound):
            usecase("nobody@example.com")
