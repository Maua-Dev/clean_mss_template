from .get_items_by_type_controller import GetItemsByTypeController
from .get_items_by_type_usecase import GetItemsByTypeUsecase
from src.shared.environments import Environments
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse
from src.shared.helpers.observability.wrap_handler import observed_handler

item_repo = Environments.get_item_repo()()
usecase = GetItemsByTypeUsecase(item_repo)
controller = GetItemsByTypeController(usecase)


@observed_handler("get_items_by_type")
def lambda_handler(event, context):
    http_request = LambdaHttpRequest(data=event)
    response = controller(http_request)
    http_response = LambdaHttpResponse(
        status_code=response.status_code,
        body=response.body,
        headers=response.headers
    )
    return http_response.toDict()
