from src.shared.helpers.errors.base_error import BaseError


class MissingParameters(BaseError):
    def __init__(self, message: str):
        super().__init__(f'Field {message} is missing')
class WrongTypeParameter(BaseError):
    def __init__(self, fieldName: str, fieldTypeExpected: str, fieldTypeReceived: str):
        message = (
            f"The field '{fieldName}' has the wrong type. "
            f"Received: '{fieldTypeReceived}'. Expected: '{fieldTypeExpected}'."
        )
        super().__init__(message)
   