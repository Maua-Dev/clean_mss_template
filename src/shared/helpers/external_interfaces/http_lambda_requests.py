import json
from typing import Any

from src.shared.helpers.auth.authorizer_user import (
    USER_FROM_AUTHORIZER_KEY,
    parse_authorizer_user_from_event,
)
from src.shared.helpers.external_interfaces.http_models import HttpRequest, HttpResponse


class LambdaHttpResponse(HttpResponse):
    """
    A class to represent an HTTP response for lambda URL.
    docs: https://docs.aws.amazon.com/lambda/latest/dg/lambda-urls.html
    """
    status_code: int = 200
    body: Any = {"message": "No response"}
    headers: dict = {"Content-Type": "application/json"}

    def __init__(
        self, 
        body: Any = None, 
        status_code: int = None, 
        headers: dict = None, 
        **kwargs
    ) -> None:
        """
        Constructor for LambdaHttpResponse.
        Args:
            body: The body of the response. Can be a string or a dict.
            status_code: The status code of the response. Defaults to 200.
            headers: The headers of the response. Defaults to {"Content-Type": "application/json"}.
            **kwargs: Configuration of the HTTP response. Possible values: add_default_cors_headers (default is True)
        """
        _body = LambdaHttpResponse.body if body is None else body
        _headers = dict(headers) if headers is not None else dict(LambdaHttpResponse.headers)
        _status_code = LambdaHttpResponse.status_code if status_code is None else status_code

        if kwargs.get("add_default_cors_headers", True):
            _headers["Access-Control-Allow-Origin"] = "*"

        super().__init__(body=_body, headers=_headers, status_code=_status_code)

    def toDict(self) -> dict:
        """
        Returns a dict representation of the HttpResponse.
        Returns:
            {
                'statusCode': int
                'body': str or dict
                'headers': dict
                'isBase64Encoded': bool
            }
        """
        return {
            "statusCode": self.status_code,
            "body": json.dumps(self.body),
            "headers": self.headers,
            "isBase64Encoded": False
        }

    def __repr__(self):
        return (
            f"HttpResponse (status_code={self.status_code}, body={self.body}, headers={self.headers})"
        )


class LambdaDefaultHTTP:
    method: str = ""
    path: str = ""
    protocol: str = ""
    source_ip: str = ""
    user_agent: str = ""

    def __init__(self, data: dict = None) -> None:
        """
        Constructor for LambdaDefaultHTTP.
        Args:
            data: dict - the "http" section of the lambda event requestContext.
        """
        if not data:
            return
        self.method = data.get("method") or ""
        self.path = data.get("path") or ""
        self.protocol = data.get("protocol") or ""
        self.source_ip = data.get("sourceIp") or ""
        self.user_agent = data.get("userAgent") or ""

    def __eq__(self, other):
        if not isinstance(other, LambdaDefaultHTTP):
            return False
        return self.method == other.method and self.path == other.path and self.protocol == other.protocol and self.source_ip == other.source_ip and self.user_agent == other.user_agent


class LambdaHttpRequest(HttpRequest):
    """
    A class to represent an HTTP request for lambda URL.
    docs: https://docs.aws.amazon.com/lambda/latest/dg/lambda-urls.html
    """
    version: str
    raw_path: str
    raw_query_string: str
    headers: dict
    query_string_parameters: dict
    request_context: dict
    http: LambdaDefaultHTTP
    body: Any

    def __init__(self, data: dict = None) -> None:
        """
        Constructor for LambdaHttpRequest.
        Args:
            data: dict - the event passed to the lambda function.
        """
        _headers = data.get("headers")
        _query_string_parameters = data.get("queryStringParameters")
        _body = None

        if "body" in data:
            try:
                _body = json.loads(data.get("body"))
            except:
                _body = data.get("body")

        super().__init__(body=_body, headers=_headers, query_params=_query_string_parameters)

        self.version = data.get("version")
        self.raw_path = data.get("rawPath")
        self.raw_query_string = data.get("rawQueryString")
        self.query_string_parameters = data.get("queryStringParameters")
        self.request_context = data.get("requestContext")
        self.http = LambdaDefaultHTTP(self.request_context.get("http") if self.request_context else None)

        # injeta DEPOIS do body/query para o cliente não spoofar via payload
        authorizer_user = parse_authorizer_user_from_event(data)
        if authorizer_user is not None:
            self.data[USER_FROM_AUTHORIZER_KEY] = authorizer_user
        else:
            self.data.pop(USER_FROM_AUTHORIZER_KEY, None)
