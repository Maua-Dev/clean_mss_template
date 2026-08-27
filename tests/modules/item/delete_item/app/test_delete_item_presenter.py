import json
import os

os.environ["STAGE"] = "TEST"

from src.modules.item.delete_item.app.delete_item_presenter import lambda_handler

_ADMIN_CONTEXT = json.dumps({
    "sub": "ms-admin",
    "mail": "alice@example.com",
    "name": "Alice Admin",
})


class Test_DeleteItemPresenter:
    def test_delete_item(self):
        event = {
            "version": "2.0",
            "routeKey": "$default",
            "rawPath": "/items/11111111-1111-4111-8111-111111111111",
            "rawQueryString": "",
            "headers": {},
            "queryStringParameters": None,
            "requestContext": {
                "accountId": "123456789012",
                "apiId": "<urlid>",
                "domainName": "<url-id>.lambda-url.us-west-2.on.aws",
                "domainPrefix": "<url-id>",
                "http": {
                    "method": "DELETE",
                    "path": "/items/11111111-1111-4111-8111-111111111111",
                    "protocol": "HTTP/1.1",
                    "sourceIp": "123.123.123.123",
                    "userAgent": "agent"
                },
                "authorizer": {"user": _ADMIN_CONTEXT},
                "requestId": "id",
                "routeKey": "$default",
                "stage": "$default",
                "time": "12/Mar/2020:19:03:58 +0000",
                "timeEpoch": 1583348638390
            },
            "body": None,
            "pathParameters": {"item_id": "11111111-1111-4111-8111-111111111111"},
            "isBase64Encoded": None,
            "stageVariables": None
        }

        response = lambda_handler(event, None)

        assert response["statusCode"] == 204
        assert response["body"] in ("null", "{}", "\"\"", "")
