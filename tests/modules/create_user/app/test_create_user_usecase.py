import pytest

from src.modules.create_user.app.create_user_usecase import CreateUserUsecase
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_CreateUserUsecase:

    def test_create_user(self):
        repo = UserRepositoryMock()
        usecase = CreateUserUsecase(repo)

        user = usecase(name="Vitor Choueri", email="branco@branco.branco")

        assert repo.users[-1] == user

    def test_create_user_invalid_name(self):
        repo = UserRepositoryMock()
        usecase = CreateUserUsecase(repo)

        with pytest.raises(EntityError):
            user = usecase(name="V", email="branco@branco.branco")

    def test_create_user_invalid_email(self):
        repo = UserRepositoryMock()
        usecase = CreateUserUsecase(repo)

        with pytest.raises(EntityError):
            user = usecase(name="Vitor Choueri", email="branco@brancobranco")


