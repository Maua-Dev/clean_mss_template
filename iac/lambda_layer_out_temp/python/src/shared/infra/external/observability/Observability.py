import time
from aws_lambda_powertools import Logger, Tracer, Metrics

class Observability():
    tracer: Tracer
    logger: Logger
    metrics: Metrics
    
    def __init__(self, tracer: Tracer = None, logger: Logger = None, metrics: Metrics = None, is_test: bool = False):
        self.tracer = tracer
        self.logger = logger
        self.metrics = metrics
        self.is_test = is_test
    
    def logger_info(self, message: str):
        if not self.is_test:
            self.logger.info(message)
            
    def logger_exception(self, message: str):
        if not self.is_test:
            self.logger.exception(message)
            
    def metrics_add_metric(self, name: str, unit: str, value: float):
        if not self.is_test:
            self.metrics.add_metric(name, unit, value)
            
    def metrics_processing_time(self, presenter):
        def presenter_wrapper(event):    
            start_time = time.monotonic() # Start - ProcessingTime metrics
            
            response = presenter(event)
            
            end_time = time.monotonic()
            processing_time_ms = (end_time - start_time) * 10**3
            
            self.metrics.add_metric(name="ProcessingTime", unit="Milliseconds", value=processing_time_ms) # End - ProcessingTime metrics
            
            return response
        return presenter_wrapper