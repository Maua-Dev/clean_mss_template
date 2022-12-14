from src.modules.update_user.app.update_user_controller import UpdateUserController
from src.modules.update_user.app.update_user_usecase import UpdateUserUsecase
from src.shared.helpers.http.http_models import HttpRequest
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_UpdateUserController:
    def test_update_user_controller(self):
        repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(repo=repo)
        controller = UpdateUserController(usecase=usecase)

        request = HttpRequest(body={
            'idUser': "1",
            'new_name': 'Branco do Branco Branco da Silva'
        })

        response = controller(request=request)

        assert response.status_code == 200
        assert response.body['idUser'] == repo.users[0].idUser
        assert response.body['name'] == 'Branco do Branco Branco da Silva'
        assert response.body['email'] == repo.users[0].email
        assert response.body['state'] == repo.users[0].state.value
        assert response.body['message'] == "the user was updated successfully"

    def test_update_user_controller_missing_idUser(self):
        repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(repo=repo)
        controller = UpdateUserController(usecase=usecase)

        request = HttpRequest(body={
            'new_name': 'Branco do Branco Branco da Silva'
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "Field idUser is missing"

    def test_update_user_controller_missing_new_name(self):
        repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(repo=repo)
        controller = UpdateUserController(usecase=usecase)

        request = HttpRequest(body={
            'idUser': "1"
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "Field new_name is missing"

    def test_update_user_controller_invalid_idUser(self):
        repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(repo=repo)
        controller = UpdateUserController(usecase=usecase)

        request = HttpRequest(body={
            'idUser': 3,
            'new_name': 'Branco do Branco Branco da Silva'
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "Field idUser isn't in the right type.\n Received: int.\n Expected: str"

    def test_update_user_not_found(self):
        repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(repo=repo)
        controller = UpdateUserController(usecase=usecase)

        request = HttpRequest(body={
            'idUser': "69",
            'new_name': 'Branco do Branco Branco da Silva'
        })

        response = controller(request=request)

        assert response.status_code == 404
        assert response.body == 'No items found for idUser'
