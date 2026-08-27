from .get_user_by_email_controller import GetUserByEmailController
from .get_user_by_email_usecase import GetUserByEmailUsecase
from src.shared.environments import Environments
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse
from src.shared.helpers.observability.wrap_handler import observed_handler

user_repo = Environments.get_user_repo()()
usecase = GetUserByEmailUsecase(user_repo)
controller = GetUserByEmailController(usecase)


@observed_handler("get_user_by_email")
def lambda_handler(event, context):
    http_request = LambdaHttpRequest(data=event)
    response = controller(http_request)
    http_response = LambdaHttpResponse(
        status_code=response.status_code,
        body=response.body,
        headers=response.headers
    )
    return http_response.toDict()
