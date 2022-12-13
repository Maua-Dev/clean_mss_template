from src.modules.create_user.app.create_user_controller import CreateUserController
from src.modules.create_user.app.create_user_usecase import CreateUserUsecase
from src.shared.helpers.http.http_models import HttpRequest
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_CreateUserControler:
    def test_create_user_controller(self):
        repo = UserRepositoryMock()
        usecase = CreateUserUsecase(repo=repo)
        controller = CreateUserController(usecase=usecase)

        request = HttpRequest(query_params={
            'name': 'Branco do Branco Branco da Silva',
            'email': 'branco@branco.com'
        })

        response = controller(request=request)

        assert response.status_code == 201
        assert response.body['idUser'] == repo.users[-1].idUser
        assert response.body['name'] == repo.users[-1].name
        assert response.body['email'] == repo.users[-1].email
        assert response.body['state'] == repo.users[-1].state.value
        assert response.body['message'] == "the user was created successfully"

    def test_create_user_controller_missing_name(self):
        repo = UserRepositoryMock()
        usecase = CreateUserUsecase(repo=repo)
        controller = CreateUserController(usecase=usecase)

        request = HttpRequest(query_params={
            'email': '21.01444-2@maua.br'})

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "Field name is missing"


    def test_create_user_controller_missing_email(self):
        repo = UserRepositoryMock()
        usecase = CreateUserUsecase(repo=repo)
        controller = CreateUserController(usecase=usecase)

        request = HttpRequest(query_params={
            'name': 'Branco do Branco Branco da Silva'})

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "Field email is missing"

    def test_create_user_controller_invalid_email(self):
        repo = UserRepositoryMock()
        usecase = CreateUserUsecase(repo=repo)
        controller = CreateUserController(usecase=usecase)

        request = HttpRequest(query_params={
            'name': 'Branco do Branco Branco da Silva',
            'email': 'branco@branco'})

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "Field email is not valid"

    def test_create_user_controller_invalid_name(self):
        repo = UserRepositoryMock()
        usecase = CreateUserUsecase(repo=repo)
        controller = CreateUserController(usecase=usecase)

        request = HttpRequest(query_params={
            'name': 'B',
            'email': 'branco@branco.com'})

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "Field name is not valid"





