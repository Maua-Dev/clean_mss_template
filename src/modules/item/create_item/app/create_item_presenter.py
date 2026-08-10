from .create_item_controller import CreateItemController
from .create_item_usecase import CreateItemUsecase
from src.shared.environments import Environments
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse

repo = Environments.get_item_repo()()
usecase = CreateItemUsecase(repo)
controller = CreateItemController(usecase)

def lambda_handler(event, context):

    from pprint import pprint

    pprint(event)

    httpRequest = LambdaHttpRequest(data=event)
    response = controller(httpRequest)
    httpResponse = LambdaHttpResponse(status_code=response.status_code, body=response.body, headers=response.headers)

    return httpResponse.toDict()

