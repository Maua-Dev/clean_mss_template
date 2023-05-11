import pytest

from src.modules.get_all_users.app.get_all_users_usecase import GetAllUsersUsecase
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_GetAllUsersUsecase:

    def test_get_all_users_usecase(self):
        repo_mock = UserRepositoryMock()
        usecase = GetAllUsersUsecase(repo_mock)

        all_users_list_returned = usecase()

        assert all_users_list_returned == repo_mock.users
        assert len(all_users_list_returned) == len(repo_mock.users)
        
    def test_usecase_must_return_an_empty_list_when_repo_return_none(self):
        repo_mock = UserRepositoryMock()
        usecase = GetAllUsersUsecase(repo_mock)

        repo_mock.users = None
        all_users_list_returned = usecase()

        assert all_users_list_returned == []


