from .get_item_controller import GetItemController
from .get_item_usecase import GetItemUsecase
from src.shared.environments import Environments
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse
from src.shared.helpers.observability.wrap_handler import observed_handler

item_repo = Environments.get_item_repo()()
usecase = GetItemUsecase(item_repo)
controller = GetItemController(usecase)


@observed_handler("get_item")
def lambda_handler(event, context):
    http_request = LambdaHttpRequest(data=event)
    response = controller(http_request)
    http_response = LambdaHttpResponse(
        status_code=response.status_code,
        body=response.body,
        headers=response.headers
    )
    return http_response.toDict()
