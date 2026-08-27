from .delete_item_controller import DeleteItemController
from .delete_item_usecase import DeleteItemUsecase
from src.shared.environments import Environments
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse
from src.shared.helpers.observability.wrap_handler import observed_handler

item_repo = Environments.get_item_repo()()
user_repo = Environments.get_user_repo()()
usecase = DeleteItemUsecase(item_repo, user_repo)
controller = DeleteItemController(usecase)


@observed_handler("delete_item")
def lambda_handler(event, context):
    http_request = LambdaHttpRequest(data=event)
    response = controller(http_request)
    http_response = LambdaHttpResponse(
        status_code=response.status_code,
        body=response.body,
        headers=response.headers
    )
    return http_response.toDict()
