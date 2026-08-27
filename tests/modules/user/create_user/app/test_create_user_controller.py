from src.modules.user.create_user.app.create_user_controller import CreateUserController
from src.modules.user.create_user.app.create_user_usecase import CreateUserUsecase
from src.shared.helpers.auth.authorizer_user import USER_FROM_AUTHORIZER_KEY
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_CreateUserController:
    def test_create_user_controller(self):
        user_repo = UserRepositoryMock()
        controller = CreateUserController(CreateUserUsecase(user_repo))

        response = controller(HttpRequest(body={
            USER_FROM_AUTHORIZER_KEY: {
                "sub": "aaaaaaaa-bbbb-4ccc-8ddd-eeeeeeeeeeee",
                "name": "Dave",
                "mail": "dave@example.com",
            }
        }))

        assert response.status_code == 201
        assert response.body["user_id"] == "aaaaaaaa-bbbb-4ccc-8ddd-eeeeeeeeeeee"
        assert response.body["user_name"] == "Dave"
        assert response.body["user_email"] == "dave@example.com"
        assert response.body["message"] == "the user was created successfully"

    def test_create_user_missing_authorizer(self):
        user_repo = UserRepositoryMock()
        controller = CreateUserController(CreateUserUsecase(user_repo))

        response = controller(HttpRequest(body={}))

        assert response.status_code == 400
        assert "user_from_authorizer" in response.body

    def test_create_user_duplicated_email(self):
        user_repo = UserRepositoryMock()
        controller = CreateUserController(CreateUserUsecase(user_repo))

        response = controller(HttpRequest(body={
            USER_FROM_AUTHORIZER_KEY: {
                "sub": "aaaaaaaa-bbbb-4ccc-8ddd-eeeeeeeeeeee",
                "name": "Alice Clone",
                "mail": "alice@example.com",
            }
        }))

        assert response.status_code == 409
        assert "user_email" in response.body
