from src.modules.create_user.app.create_user_controller import CreateUserController
from src.modules.create_user.app.create_user_usecase import CreateUserUsecase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_CreateUserController:
    def test_create_user_controller(self):
        repo = UserRepositoryMock()
        controller = CreateUserController(CreateUserUsecase(repo))

        response = controller(HttpRequest(body={
            "user_name": "Dave",
            "user_email": "dave@example.com",
            "user_role": "User",
        }))

        assert response.status_code == 201
        assert response.body["user_name"] == "Dave"
        assert response.body["user_email"] == "dave@example.com"
        assert response.body["message"] == "the user was created successfully"

    def test_create_user_missing_email(self):
        repo = UserRepositoryMock()
        controller = CreateUserController(CreateUserUsecase(repo))

        response = controller(HttpRequest(body={"user_name": "Dave"}))

        assert response.status_code == 400
        assert response.body == "Field user_email is missing"

    def test_create_user_duplicated_email(self):
        repo = UserRepositoryMock()
        controller = CreateUserController(CreateUserUsecase(repo))

        response = controller(HttpRequest(body={
            "user_name": "Alice Clone",
            "user_email": "alice@example.com",
        }))

        assert response.status_code == 400
        assert "user_email" in response.body
