from src.modules.get_user_by_email.app.get_user_by_email_controller import GetUserByEmailController
from src.modules.get_user_by_email.app.get_user_by_email_usecase import GetUserByEmailUsecase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_GetUserByEmailController:
    def test_get_user_by_email_controller(self):
        repo = UserRepositoryMock()
        controller = GetUserByEmailController(GetUserByEmailUsecase(repo))

        response = controller(HttpRequest(query_params={"user_email": "bob@example.com"}))

        assert response.status_code == 200
        assert response.body["user_name"] == "Bob User"
        assert response.body["message"] == "the user was retrieved successfully"

    def test_get_user_by_email_missing(self):
        repo = UserRepositoryMock()
        controller = GetUserByEmailController(GetUserByEmailUsecase(repo))

        response = controller(HttpRequest(query_params={}))

        assert response.status_code == 400
        assert response.body == "Field user_email is missing"

    def test_get_user_by_email_not_found(self):
        repo = UserRepositoryMock()
        controller = GetUserByEmailController(GetUserByEmailUsecase(repo))

        response = controller(HttpRequest(query_params={"user_email": "nobody@example.com"}))

        assert response.status_code == 404
