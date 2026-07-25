from typing import Any

from src.shared.helpers.enum.http_status_code_enum import HttpStatusCodeEnum
from src.shared.helpers.external_interfaces.http_models import HttpResponse


# 2xx - Success
class OK(HttpResponse):
    def __init__(self, body: Any = None) -> None:
        super().__init__(HttpStatusCodeEnum.OK.value, body)


class Created(HttpResponse):
    def __init__(self, body: Any = None) -> None:
        super().__init__(HttpStatusCodeEnum.CREATED.value, body)


class Accepted(HttpResponse):
    def __init__(self, body: Any = None) -> None:
        super().__init__(HttpStatusCodeEnum.ACCEPTED.value, body)


class NoContent(HttpResponse):
    def __init__(self) -> None:
        super().__init__(HttpStatusCodeEnum.NO_CONTENT.value, None)


# 3xx - Redirection
class MovedPermanently(HttpResponse):
    def __init__(self, location: str) -> None:
        super().__init__(
            HttpStatusCodeEnum.MOVED_PERMANENTLY.value,
            None,
            headers={"Location": location}
        )
        self.location = location


class Found(HttpResponse):
    def __init__(self, location: str) -> None:
        super().__init__(
            HttpStatusCodeEnum.FOUND.value,
            None,
            headers={"Location": location}
        )
        self.location = location


class RedirectResponse(HttpResponse):
    def __init__(self, location: str) -> None:
        super().__init__(
            HttpStatusCodeEnum.REDIRECT.value,
            None,
            headers={"Location": location}
        )
        self.location = location


class NotModified(HttpResponse):
    def __init__(self) -> None:
        super().__init__(HttpStatusCodeEnum.NOT_MODIFIED.value, None)


# 4xx - Client errors
class BadRequest(HttpResponse):
    def __init__(self, body: Any) -> None:
        super().__init__(HttpStatusCodeEnum.BAD_REQUEST.value, body)


class Unauthorized(HttpResponse):
    def __init__(self, body: Any) -> None:
        super().__init__(HttpStatusCodeEnum.UNAUTHORIZED.value, body)


class PaymentRequired(HttpResponse):
    def __init__(self, body: Any) -> None:
        super().__init__(HttpStatusCodeEnum.PAYMENT_REQUIRED.value, body)


class Forbidden(HttpResponse):
    def __init__(self, body: Any) -> None:
        super().__init__(HttpStatusCodeEnum.FORBIDDEN.value, body)


class NotFound(HttpResponse):
    def __init__(self, body: Any) -> None:
        super().__init__(HttpStatusCodeEnum.NOT_FOUND.value, body)


class MethodNotAllowed(HttpResponse):
    def __init__(self, body: Any) -> None:
        super().__init__(HttpStatusCodeEnum.METHOD_NOT_ALLOWED.value, body)


class NotAcceptable(HttpResponse):
    def __init__(self, body: Any) -> None:
        super().__init__(HttpStatusCodeEnum.NOT_ACCEPTABLE.value, body)


class Conflict(HttpResponse):
    def __init__(self, body: Any) -> None:
        super().__init__(HttpStatusCodeEnum.CONFLICT.value, body)


class UnsupportedMediaType(HttpResponse):
    def __init__(self, body: Any) -> None:
        super().__init__(HttpStatusCodeEnum.UNSUPPORTED_MEDIA_TYPE.value, body)


class UnprocessableEntity(HttpResponse):
    def __init__(self, body: Any) -> None:
        super().__init__(HttpStatusCodeEnum.UNPROCESSABLE_ENTITY.value, body)


class TooManyRequests(HttpResponse):
    def __init__(self, body: Any) -> None:
        super().__init__(HttpStatusCodeEnum.TOO_MANY_REQUESTS.value, body)


# 5xx - Server errors
class InternalServerError(HttpResponse):
    def __init__(self, body: Any) -> None:
        super().__init__(HttpStatusCodeEnum.INTERNAL_SERVER_ERROR.value, body)


class NotImplementedResponse(HttpResponse):
    def __init__(self, body: Any) -> None:
        super().__init__(HttpStatusCodeEnum.NOT_IMPLEMENTED.value, body)


class BadGateway(HttpResponse):
    def __init__(self, body: Any) -> None:
        super().__init__(HttpStatusCodeEnum.BAD_GATEWAY.value, body)


class ServiceUnavailable(HttpResponse):
    def __init__(self, body: Any) -> None:
        super().__init__(HttpStatusCodeEnum.SERVICE_UNAVAILABLE.value, body)


class GatewayTimeout(HttpResponse):
    def __init__(self, body: Any) -> None:
        super().__init__(HttpStatusCodeEnum.GATEWAY_TIMEOUT.value, body)
