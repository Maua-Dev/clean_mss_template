from src.modules.user.create_user.app.create_user_controller import CreateUserController
from src.modules.user.create_user.app.create_user_usecase import CreateUserUsecase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_CreateUserController:
    def test_create_user_controller(self):
        user_repo = UserRepositoryMock()
        controller = CreateUserController(CreateUserUsecase(user_repo))

        response = controller(HttpRequest(body={
            "user_id": "aaaaaaaa-bbbb-4ccc-8ddd-eeeeeeeeeeee",
            "user_name": "Dave",
            "user_email": "dave@example.com",
        }))

        assert response.status_code == 201
        assert response.body["user_id"] == "aaaaaaaa-bbbb-4ccc-8ddd-eeeeeeeeeeee"
        assert response.body["user_name"] == "Dave"
        assert response.body["user_email"] == "dave@example.com"
        assert response.body["message"] == "the user was created successfully"

    def test_create_user_missing_email(self):
        user_repo = UserRepositoryMock()
        controller = CreateUserController(CreateUserUsecase(user_repo))

        response = controller(HttpRequest(body={
            "user_id": "aaaaaaaa-bbbb-4ccc-8ddd-eeeeeeeeeeee",
            "user_name": "Dave",
        }))

        assert response.status_code == 400
        assert response.body == "Field user_email is missing"

    def test_create_user_duplicated_email(self):
        user_repo = UserRepositoryMock()
        controller = CreateUserController(CreateUserUsecase(user_repo))

        response = controller(HttpRequest(body={
            "user_id": "aaaaaaaa-bbbb-4ccc-8ddd-eeeeeeeeeeee",
            "user_name": "Alice Clone",
            "user_email": "alice@example.com",
        }))

        assert response.status_code == 400
        assert "user_email" in response.body
