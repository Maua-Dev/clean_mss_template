from src.modules.user.get_all_users.app.get_all_users_controller import GetAllUsersController
from src.modules.user.get_all_users.app.get_all_users_usecase import GetAllUsersUsecase
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_GetAllUsersController:
    def test_get_all_users_controller(self):
        repo = UserRepositoryMock()
        controller = GetAllUsersController(GetAllUsersUsecase(repo))

        response = controller(None)

        assert response.status_code == 200
        assert len(response.body["all_users"]) == 3
        assert response.body["message"] == "all users have been retrieved"
