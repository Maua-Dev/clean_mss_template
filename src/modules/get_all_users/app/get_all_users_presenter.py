from .get_all_users_controller import GetAllUsersController
from .get_all_users_usecase import GetAllUsersUsecase
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.environments import Environments
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse

repo: IUserRepository = Environments.get_user_repo()()
usecase = GetAllUsersUsecase(repo)
controller = GetAllUsersController(usecase)


def lambda_handler(event, context):
    httpRequest = LambdaHttpRequest(data=event)
    response = controller(httpRequest)
    httpResponse = LambdaHttpResponse(status_code=response.status_code, body=response.body, headers=response.headers)

    return httpResponse.toDict()
