from src.modules.user.get_user.app.get_user_controller import GetUserController
from src.modules.user.get_user.app.get_user_usecase import GetUserUsecase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_GetUserController:
    def test_get_user_controller(self):
        user_repo = UserRepositoryMock()
        controller = GetUserController(GetUserUsecase(user_repo))
        user = user_repo.users[1]

        response = controller(HttpRequest(path_params={"user_id": str(user.user_id)}))

        assert response.status_code == 200
        assert response.body["user_email"] == "bob@example.com"
        assert response.body["message"] == "the user was retrieved successfully"

    def test_get_user_missing(self):
        user_repo = UserRepositoryMock()
        controller = GetUserController(GetUserUsecase(user_repo))

        response = controller(HttpRequest(path_params={}))

        assert response.status_code == 400
        assert response.body == "Field user_id is missing"

    def test_get_user_not_found(self):
        user_repo = UserRepositoryMock()
        controller = GetUserController(GetUserUsecase(user_repo))

        response = controller(HttpRequest(path_params={
            "user_id": "99999999-9999-4999-8999-999999999999"
        }))

        assert response.status_code == 404
