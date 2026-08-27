from uuid import UUID

from src.modules.user.auth_user.app.auth_user_controller import AuthUserController
from src.modules.user.auth_user.app.auth_user_usecase import AuthUserUsecase
from src.shared.helpers.auth.authorizer_user import USER_FROM_AUTHORIZER_KEY
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_AuthUserController:
    def test_auth_user_creates(self):
        user_repo = UserRepositoryMock()
        controller = AuthUserController(AuthUserUsecase(user_repo))

        response = controller(HttpRequest(body={
            USER_FROM_AUTHORIZER_KEY: {
                "sub": "dddddddd-dddd-4ddd-8ddd-dddddddddddd",
                "mail": "dave@example.com",
                "name": "Dave",
            }
        }))

        assert response.status_code == 200
        assert response.body["user_id"] == "dddddddd-dddd-4ddd-8ddd-dddddddddddd"
        assert response.body["user_name"] == "Dave"
        assert response.body["message"] == "the user was created successfully"

    def test_auth_user_substitutes_existing(self):
        user_repo = UserRepositoryMock()
        controller = AuthUserController(AuthUserUsecase(user_repo))
        existing = user_repo.users[1]
        new_id = "eeeeeeee-eeee-4eee-8eee-eeeeeeeeeeee"

        response = controller(HttpRequest(body={
            USER_FROM_AUTHORIZER_KEY: {
                "sub": new_id,
                "mail": str(existing.user_email),
                "name": "Bob From Graph",
            }
        }))

        assert response.status_code == 200
        assert response.body["user_id"] == new_id
        assert response.body["user_name"] == "Bob From Graph"
        assert response.body["message"] == "the user was retrieved successfully"
        assert user_repo.get_user(UUID(new_id)).user_name == "Bob From Graph"

    def test_auth_user_missing_authorizer(self):
        user_repo = UserRepositoryMock()
        controller = AuthUserController(AuthUserUsecase(user_repo))

        response = controller(HttpRequest(body={}))

        assert response.status_code == 400
        assert "user_from_authorizer" in response.body
