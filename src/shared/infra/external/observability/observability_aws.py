import time
from aws_lambda_powertools import Logger, Tracer, Metrics
from src.shared.domain.observability.observability_interface import IObservability

class ObservabilityAWS(IObservability):
    tracer: Tracer
    logger: Logger
    metrics: Metrics
     
    def __init__(self, tracer: Tracer = None, logger: Logger = None, metrics: Metrics = None, is_test: bool = False):
        super().__init__(tracer=tracer, logger=logger, metrics=metrics, is_test=is_test)
    
    def log_info(self, message: str) -> None:
        if not self.is_test:
            self.logger.info(message)
            
    def log_exception(self, message: str) -> None:
        if not self.is_test:
            self.logger.exception(message)
            
    def add_metric(self, name: str, unit: str, value: float) -> None:
        if not self.is_test:
            self.metrics.add_metric(name, unit, value)
            
    def processing_time_calculation(self, presenter) -> None:
        def presenter_wrapper(event):    
            start_time = time.monotonic() # Start - ProcessingTime metrics
            
            response = presenter(event)
            
            end_time = time.monotonic()
            processing_time_ms = (end_time - start_time) * 10**3
            
            self.metrics.add_metric(name="ProcessingTime", unit="Milliseconds", value=processing_time_ms) # End - ProcessingTime metrics
            
            return response
        return presenter_wrapper