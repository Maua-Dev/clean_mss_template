import time
from aws_lambda_powertools import Logger, Tracer, Metrics
from abc import ABC, abstractmethod

class IObservability(ABC):
    @abstractmethod
    def __init__(self, service_name: str = "default-service-name") -> None:
        pass
    
    @abstractmethod
    def log_info(self, message: str) -> None:
        pass
            
    @abstractmethod
    def log_exception(self, message: str) -> None:
        pass
            
    @abstractmethod
    def add_metric(self, name: str, unit: str, value: float) -> None:
        pass
            
    @abstractmethod
    def presenter_decorators(self, presenter) -> None:
        """
        this decorator have the following responsabilities:
        1. calculate the processing time of the presenter
        2. use the @tracer.capture_method to trace the presenter
        """
        def presenter_wrapper(event):    
            pass
        pass
    
    @abstractmethod
    def handler_decorators(self, handler) -> None:
        """
        this decorator have the following responsabilities:
        1. use the @tracer.capture_lambda_handler
        2. use the @metrics.log_metrics(capture_cold_start_metric=True, default_dimensions={"environment": os.getenv("STAGE", "dev"), "another": "one"}) # ColdStart metrics and adding dimensions
        3. use the @logger.inject_lambda_context(log_event=True) # Log event
        """
        def handler_wrapper(event, context):    
            pass
        pass