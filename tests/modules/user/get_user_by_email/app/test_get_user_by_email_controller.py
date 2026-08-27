from src.modules.user.get_user_by_email.app.get_user_by_email_controller import GetUserByEmailController
from src.modules.user.get_user_by_email.app.get_user_by_email_usecase import GetUserByEmailUsecase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_GetUserByEmailController:
    def test_get_user_by_email_controller(self):
        user_repo = UserRepositoryMock()
        controller = GetUserByEmailController(GetUserByEmailUsecase(user_repo))

        response = controller(HttpRequest(query_params={"email": "bob@example.com"}))

        assert response.status_code == 200
        assert response.body["user_name"] == "Bob User"
        assert response.body["message"] == "the user was retrieved successfully"

    def test_get_user_by_email_missing(self):
        user_repo = UserRepositoryMock()
        controller = GetUserByEmailController(GetUserByEmailUsecase(user_repo))

        response = controller(HttpRequest(query_params={}))

        assert response.status_code == 400
        assert response.body == "Field email is missing"

    def test_get_user_by_email_not_found(self):
        user_repo = UserRepositoryMock()
        controller = GetUserByEmailController(GetUserByEmailUsecase(user_repo))

        response = controller(HttpRequest(query_params={"email": "nobody@example.com"}))

        assert response.status_code == 404
