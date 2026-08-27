import pytest

from src.modules.user.get_user_by_email.app.get_user_by_email_usecase import GetUserByEmailUsecase
from src.shared.helpers.errors.usecase_errors import NoUsersFound
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_GetUserByEmailUsecase:
    def test_get_user_by_email(self):
        user_repo = UserRepositoryMock()
        usecase = GetUserByEmailUsecase(user_repo)

        user = usecase("alice@example.com")

        assert user.user_name == "Alice Admin"

    def test_get_user_by_email_not_found(self):
        user_repo = UserRepositoryMock()
        usecase = GetUserByEmailUsecase(user_repo)

        with pytest.raises(NoUsersFound):
            usecase("nobody@example.com")
