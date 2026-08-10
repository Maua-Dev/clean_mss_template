from .get_all_items_controller import GetAllItemsController
from .get_all_items_usecase import GetAllItemsUsecase
from src.shared.domain.repositories.item_repository_interface import IItemRepository
from src.shared.environments import Environments
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse
from src.shared.helpers.observability.wrap_handler import observed_handler

repo: IItemRepository = Environments.get_item_repo()()
usecase = GetAllItemsUsecase(repo)
controller = GetAllItemsController(usecase)


@observed_handler("get_all_items")
def lambda_handler(event, context):
    http_request = LambdaHttpRequest(data=event)
    response = controller(http_request)
    http_response = LambdaHttpResponse(
        status_code=response.status_code,
        body=response.body,
        headers=response.headers
    )
    return http_response.toDict()
