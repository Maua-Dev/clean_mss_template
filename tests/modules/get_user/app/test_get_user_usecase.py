import pytest

from src.modules.get_user.app.get_user_usecase import GetUserUsecase
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_GetUserUsecase:

    def test_get_user(self):
        repo = UserRepositoryMock()
        usecase = GetUserUsecase(repo)

        user = usecase(user_id=repo.users[1].user_id)

        assert repo.users[1] == user

    def test_get_user_not_found(self):
        repo = UserRepositoryMock()
        usecase = GetUserUsecase(repo)

        with pytest.raises(NoItemsFound):
            user = usecase(user_id=999)

    def test_get_user_invalid_id(self):
        repo = UserRepositoryMock()
        usecase = GetUserUsecase(repo)

        with pytest.raises(EntityError):
            user = usecase(user_id="invalid")
