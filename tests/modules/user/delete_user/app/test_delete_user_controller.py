from src.modules.user.delete_user.app.delete_user_controller import DeleteUserController
from src.modules.user.delete_user.app.delete_user_usecase import DeleteUserUsecase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_DeleteUserController:
    def test_delete_user_controller(self):
        user_repo = UserRepositoryMock()
        controller = DeleteUserController(DeleteUserUsecase(user_repo))
        user_id = str(user_repo.users[0].user_id)

        response = controller(HttpRequest(body={"user_id": user_id}))

        assert response.status_code == 204
        assert not response.body

    def test_delete_user_not_found(self):
        user_repo = UserRepositoryMock()
        controller = DeleteUserController(DeleteUserUsecase(user_repo))

        response = controller(HttpRequest(body={
            "user_id": "99999999-9999-4999-8999-999999999999"
        }))

        assert response.status_code == 404
