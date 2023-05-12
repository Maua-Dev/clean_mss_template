from src.modules.get_all_users.app.get_all_users_controller import GetAllUsersController
from src.modules.get_all_users.app.get_all_users_usecase import GetAllUsersUsecase
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_GetAllUsersController:

    def test_get_all_users_controller(self):
        repo_mock = UserRepositoryMock()
        get_all_users_usecase = GetAllUsersUsecase(repo_mock)
        controller = GetAllUsersController(get_all_users_usecase)

        response = controller(None)

        assert response.status_code == 200

