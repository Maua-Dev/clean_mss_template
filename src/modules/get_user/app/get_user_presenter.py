import os
from .get_user_controller import GetUserController
from .get_user_usecase import GetUserUsecase
from src.shared.environments import Environments
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse
import time

from aws_lambda_powertools import Logger, Tracer, Metrics

logger = Logger(service="TEST-OBSERVABILITY")
tracer = Tracer(service="TEST-OBSERVABILITY")
metrics = Metrics(namespace="TEST-OBSERVABILITY")

repo = Environments.get_user_repo()()
usecase = GetUserUsecase(repo)
controller = GetUserController(usecase, logger=logger)

def get_user_presenter(event):
    httpRequest = LambdaHttpRequest(data=event)
    response = controller(httpRequest)
    httpResponse = LambdaHttpResponse(status_code=response.status_code, body=response.body, headers=response.headers)
    return httpResponse.toDict()
    
# @tracer.capture_lambda_handler
@metrics.log_metrics(capture_cold_start_metric=True, default_dimensions={"environment": os.getenv("STAGE", "dev"), "another": "one"}) # ColdStart metrics and adding dimensions
@logger.inject_lambda_context(log_event=True) # Log event
def lambda_handler(event, context):
    start_time = time.monotonic() # Start - ProcessingTime metrics
    
    response = get_user_presenter(event)
    
    end_time = time.monotonic()
    processing_time_ms = (end_time - start_time) * 10**3
    metrics.add_metric(name="ProcessingTime", unit="Milliseconds", value=processing_time_ms) # End - ProcessingTime metrics
    
    metrics.add_metric(name="ErrorCount", unit="Count", value=1) if response["statusCode"] != 200 else None # ErrorCount metrics
    
    return response

