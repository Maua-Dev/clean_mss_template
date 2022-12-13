from typing import Any

from src.shared.helpers.enum.http_status_code_enum import HttpStatusCodeEnum


class HttpRequest:
    body: dict
    headers: dict
    query_params: dict

    def __init__(self, body: dict = None, headers: dict = None, query_params: dict = None):
        self.body = body
        self.headers = headers
        self.query_params = query_params

    def __repr__(self):
        return (
            f"HttpRequest (body={self.body}, headers={self.headers}, query_params={self.query_params})"
        )


class HttpResponse:
    status_code: int
    body: dict
    headers: dict

    def __init__(self, status_code: int, body: dict = None, headers: dict = None):
        self.status_code = status_code
        self.body = body
        self.headers = headers

    def __repr__(self):
        return (
            f"HttpResponse (status_code={self.status_code}, body={self.body}, headers={self.headers})"
        )


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
