import time
from aws_lambda_powertools import Logger, Tracer, Metrics
from abc import ABC, abstractmethod

class IObservability(ABC):
    tracer: Tracer
    logger: Logger
    metrics: Metrics
    
    def __init__(self, tracer: Tracer = None, logger: Logger = None, metrics: Metrics = None, is_test: bool = False):
        self.tracer = tracer
        self.logger = logger
        self.metrics = metrics
        self.is_test = is_test
        
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
    def processing_time_calculation(self, presenter) -> None:
        def presenter_wrapper(event):    
            pass
        pass