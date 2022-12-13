from src.shared.domain.enums.state_enum import STATE
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock
import pytest


class Test_UserRepositoryMock:
    def test_get_user(self):
        repo = UserRepositoryMock()
        user = repo.get_user(1)

        assert user.name == "Bruno Soller"
        assert user.email == "soller@soller.com"
        assert user.idUser == 1
        assert user.state == STATE.APPROVED

    def test_get_user_not_found(self):
        repo = UserRepositoryMock()
        with pytest.raises(NoItemsFound):
            user = repo.get_user(69)
