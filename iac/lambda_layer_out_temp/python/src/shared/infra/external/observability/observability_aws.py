import os
import time
from aws_lambda_powertools import Logger, Tracer, Metrics
from src.shared.domain.observability.observability_interface import IObservability

class ObservabilityAWS(IObservability):
    tracer: Tracer
    logger: Logger
    metrics: Metrics
     
    def __init__(self, service_name: str = "default-service-name"):
        self.logger = Logger(service=service_name)
        self.tracer = Tracer(service=service_name)
        self.metrics = Metrics(namespace=service_name)
    
    def log_info(self, message: str) -> None:
        self.logger.info(message)
            
    def log_exception(self, message: str) -> None:
        self.logger.exception(message)
            
    def add_metric(self, name: str, unit: str, value: float) -> None:
        self.metrics.add_metric(name, unit, value)
            
    
    def presenter_decorators(self, presenter) -> None:
        # @self.tracer.capture_method
        def presenter_wrapper(event):    
            start_time = time.monotonic() # Start - ProcessingTime metrics
            
            response = presenter(event)
            
            end_time = time.monotonic()
            processing_time_ms = (end_time - start_time) * 10**3
            
            self.metrics.add_metric(name="ProcessingTime", unit="Milliseconds", value=processing_time_ms) # End - ProcessingTime metrics
            
            return response
        return presenter_wrapper
    
    def handler_decorators(self, handler) -> None:
        # @self.tracer.capture_lambda_handler
        @self.metrics.log_metrics(capture_cold_start_metric=True, default_dimensions={"environment": os.getenv("STAGE", "dev"), "another": "one"}) # ColdStart metrics and adding dimensions
        @self.logger.inject_lambda_context(log_event=True) # Log event
        def handler_wrapper(event, context):    
            
            response = handler(event, context)
            
            return response
        return handler_wrapper