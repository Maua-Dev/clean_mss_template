from src.modules.update_user.app.update_user_controller import UpdateUserController
from src.modules.update_user.app.update_user_usecase import UpdateUserUsecase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_UpdateUserController:
    def test_update_user_controller(self):
        repo = UserRepositoryMock()
        controller = UpdateUserController(UpdateUserUsecase(repo))
        user = repo.users[0]

        response = controller(HttpRequest(body={
            "user_id": str(user.user_id),
            "user_name": "Alice Updated",
            "user_email": "alice.updated@example.com",
            "user_role": "Admin",
        }))

        assert response.status_code == 200
        assert response.body["user_name"] == "Alice Updated"
        assert response.body["message"] == "the user was updated successfully"

    def test_update_user_not_found(self):
        repo = UserRepositoryMock()
        controller = UpdateUserController(UpdateUserUsecase(repo))

        response = controller(HttpRequest(body={
            "user_id": "99999999-9999-4999-8999-999999999999",
            "user_name": "Ghost",
            "user_email": "ghost@example.com",
            "user_role": "User",
        }))

        assert response.status_code == 404
