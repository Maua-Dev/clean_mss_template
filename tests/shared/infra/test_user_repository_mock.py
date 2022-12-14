from src.shared.domain.entities.user import User
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

    def test_get_all_user(self):
        repo = UserRepositoryMock()
        users = repo.get_all_user()
        assert len(users) == 3

    def test_create_user(self):
        repo = UserRepositoryMock()
        user = User(
            name="Vitor Soller",
            email="dohype@vitin.com",
            idUser=4,
            state=STATE.PENDING
        )

    def test_delete_user(self):
        repo = UserRepositoryMock()
        user = repo.delete_user(1)
        assert user.name == "Bruno Soller"
        assert user.email == "soller@soller.com"
        assert user.idUser == 1
        assert user.state == STATE.APPROVED

    def test_delete_user_not_found(self):
        repo = UserRepositoryMock()
        with pytest.raises(NoItemsFound):
            user = repo.delete_user(69)

