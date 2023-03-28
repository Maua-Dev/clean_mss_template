import os
from .get_user_controller import GetUserController
from .get_user_usecase import GetUserUsecase
from src.shared.environments import Environments
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse
import time
from src.shared.infra.external.observability.observability_aws import ObservabilityAWS
from aws_lambda_powertools import Logger, Tracer, Metrics

logger = Logger(service="TEST-OBSERVABILITY")
tracer = Tracer(service="TEST-OBSERVABILITY")
metrics = Metrics(namespace="TEST-OBSERVABILITY")

observability = ObservabilityAWS(tracer=tracer, logger=logger, metrics=metrics)

repo = Environments.get_user_repo()()
usecase = GetUserUsecase(repo, observability=observability)
controller = GetUserController(usecase, observability=observability)

@tracer.capture_method
@observability.processing_time_calculation
def get_user_presenter(event):
    httpRequest = LambdaHttpRequest(data=event)
    response = controller(httpRequest)
    httpResponse = LambdaHttpResponse(status_code=response.status_code, body=response.body, headers=response.headers)
    return httpResponse.toDict()
    
@tracer.capture_lambda_handler
@metrics.log_metrics(capture_cold_start_metric=True, default_dimensions={"environment": os.getenv("STAGE", "dev"), "another": "one"}) # ColdStart metrics and adding dimensions
@logger.inject_lambda_context(log_event=True) # Log event
def lambda_handler(event, context):
    
    response = get_user_presenter(event)
    
    observability.add_metric(name="ErrorCount", unit="Count", value=1) if response["statusCode"] != 200 else None # ErrorCount metrics
    
    return response

