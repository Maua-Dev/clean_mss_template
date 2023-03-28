from src.shared.domain.observability.observability_interface import IObservability


class ObservabilityMock(IObservability):
    service_name: str
    
    def __init__(self, service_name: str = "default-service-name") -> None:
        self.service_name = service_name
    
    def log_info(self, message: str) -> None:
        print("Logging the following message: " + message)
            
    def log_exception(self, message: str) -> None:
        print("Exception message: " + message)
            
    def add_metric(self, name: str, unit: str, value: float) -> None:
        print(f"Metric {name} added with value {value} in {unit}")
            
    def presenter_decorators(self, presenter) -> None:
        def presenter_wrapper(event):    
            response = presenter(event)
            
            return response
        return presenter_wrapper
    
    def handler_decorators(self, handler) -> None:
        def handler_wrapper(event, context):    
            response = handler(event, context)
            
            return response
        return handler_wrapper