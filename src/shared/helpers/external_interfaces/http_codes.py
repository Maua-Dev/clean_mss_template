from typing import Any

from src.shared.helpers.enum.http_status_code_enum import HttpStatusCodeEnum
from src.shared.helpers.external_interfaces.http_models import HttpResponse


class OK(HttpResponse):
    def __init__(self, body: Any = None) -> None:
        super().__init__(HttpStatusCodeEnum.OK.value, body)


class Created(HttpResponse):
    def __init__(self, body: Any = None) -> None:
        super().__init__(HttpStatusCodeEnum.CREATED.value, body)


class NoContent(HttpResponse):
    def __init__(self) -> None:
        super().__init__(HttpStatusCodeEnum.NO_CONTENT.value, None)


class BadRequest(HttpResponse):
    def __init__(self, body: Any) -> None:
        super().__init__(HttpStatusCodeEnum.BAD_REQUEST.value, body)


class InternalServerError(HttpResponse):
    def __init__(self, body: Any) -> None:
        super().__init__(HttpStatusCodeEnum.INTERNAL_SERVER_ERROR.value, body)


class NotFound(HttpResponse):
    def __init__(self, body: Any) -> None:
        super().__init__(HttpStatusCodeEnum.NOT_FOUND.value, body)


class Conflict(HttpResponse):
    def __init__(self, body: Any) -> None:
        super().__init__(HttpStatusCodeEnum.CONFLICT.value, body)


class RedirectResponse(HttpResponse):
    def __init__(self, body: dict) -> None:
        super().__init__(HttpStatusCodeEnum.REDIRECT.value, None)
        self.location = body


class Forbidden(HttpResponse):
    def __init__(self, body: dict) -> None:
        super().__init__(HttpStatusCodeEnum.FORBIDDEN.value, body)
