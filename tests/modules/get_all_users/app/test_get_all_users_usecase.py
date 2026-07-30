from src.modules.get_all_users.app.get_all_users_usecase import GetAllUsersUsecase
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_GetAllUsersUsecase:
    def test_get_all_users(self):
        repo = UserRepositoryMock()
        assert len(GetAllUsersUsecase(repo)()) == 3
