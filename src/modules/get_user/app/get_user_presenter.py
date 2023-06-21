from .get_user_controller import GetUserController
from .get_user_usecase import GetUserUsecase
from src.shared.environments import Environments
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse
from src.shared.infra.external.observability.observability_aws import ObservabilityAWS
from aws_lambda_powertools import Logger, Tracer, Metrics


observability = Environments.get_observability()(module_name="get_user")

repo = Environments.get_user_repo()()
usecase = GetUserUsecase(repo, observability=observability)
controller = GetUserController(usecase, observability=observability)

@observability.presenter_decorators
def get_user_presenter(event):
    httpRequest = LambdaHttpRequest(data=event)
    response = controller(httpRequest)
    httpResponse = LambdaHttpResponse(status_code=response.status_code, body=response.body, headers=response.headers)
    return httpResponse.toDict()

@observability.handler_decorators
def lambda_handler(event, context):
    
    response = get_user_presenter(event)
    
    observability.add_metric(name="ErrorCount", unit="Count", value=1) if response["statusCode"] != 200 else None # ErrorCount metrics
    
    return response

