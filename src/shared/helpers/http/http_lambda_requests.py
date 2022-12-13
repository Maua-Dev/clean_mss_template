import json

from src.shared.helpers.http.http_models import HttpRequest, HttpResponse


class LambdaHttpResponse(HttpResponse):
    """
    A class to represent an HTTP response for lambda URL.
    docs: https://docs.aws.amazon.com/lambda/latest/dg/lambda-urls.html
    """
    status_code: int = 200
    body: any = {"message": "No response"}
    headers: dict = {"Content-Type": "application/json"}

    def __init__(self, body: any = None, status_code: int = None, headers: dict = None, **kwargs) -> None:
        """
        Constructor for HttpResponse.
        Args:
            body: The body of the response. Can be a string or a dict.
            status_code: The status code of the response. Defaults to 200.
            headers: The headers of the response. Defaults to {"Content-Type": "application/json"}.
            **kwargs: Configuration of the HTTP response. Possible values: add_default_cors_headers (default is True)
        """
        _body = body or LambdaHttpResponse.body
        _headers = headers or LambdaHttpResponse.headers
        _headers['Access-Control-Allow-Origin'] = '*'
        
        _status_code = status_code or LambdaHttpResponse.status_code

        if kwargs.get("add_default_cors_headers", True):
            _headers.update({"Access-Control-Allow-Origin": "*"})

        super().__init__(body=_body, headers=_headers, status_code=_status_code)

    def toDict(self) -> dict:
        """
        Returns a dict representation of the HttpResponse.
        Returns:
            {
                'statuCode': int
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
        Constructor for LambdaHttp.
        Args:
            event: dict - the event passed to the lambda function.
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
    body: any

    def __init__(self, data: dict = None) -> None:
        """
        Constructor for HttpResponse.
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

class HttpResponseRedirect(HttpResponse):

    def __init__(self, location: str) -> None:
        super().__init__(status_code=302, headers={"Location": location})
