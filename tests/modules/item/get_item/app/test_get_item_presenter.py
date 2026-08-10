import json
import os

os.environ["STAGE"] = "TEST"

from src.modules.item.get_item.app.get_item_presenter import lambda_handler


class Test_GetItemPresenter:
    def test_get_item(self):
        event = {
            "version": "2.0",
            "routeKey": "$default",
            "rawPath": "/my/path",
            "rawQueryString": "item_id=11111111-1111-4111-8111-111111111111",
            "headers": {},
            "queryStringParameters": {
                "item_id": "11111111-1111-4111-8111-111111111111"
            },
            "requestContext": {
                "accountId": "123456789012",
                "apiId": "<urlid>",
                "domainName": "<url-id>.lambda-url.us-west-2.on.aws",
                "domainPrefix": "<url-id>",
                "http": {
                    "method": "GET",
                    "path": "/my/path",
                    "protocol": "HTTP/1.1",
                    "sourceIp": "123.123.123.123",
                    "userAgent": "agent"
                },
                "requestId": "id",
                "routeKey": "$default",
                "stage": "$default",
                "time": "12/Mar/2020:19:03:58 +0000",
                "timeEpoch": 1583348638390
            },
            "body": None,
            "pathParameters": None,
            "isBase64Encoded": None,
            "stageVariables": None
        }

        response = lambda_handler(event, None)
        body = json.loads(response["body"])

        assert response["statusCode"] == 200
        assert body["item_name"] == "Notebook"
        assert body["item_type"] == "type1"
        assert body["item_id"] == "11111111-1111-4111-8111-111111111111"
        assert body["message"] == "the item was retrieved successfully"
