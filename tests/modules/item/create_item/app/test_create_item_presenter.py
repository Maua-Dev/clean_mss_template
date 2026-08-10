import json
import os

os.environ["STAGE"] = "TEST"

from src.modules.item.create_item.app.create_item_presenter import lambda_handler


class Test_CreateItemPresenter:
    def test_create_item(self):
        event = {
            "version": "2.0",
            "routeKey": "$default",
            "rawPath": "/my/path",
            "rawQueryString": "",
            "headers": {},
            "queryStringParameters": None,
            "requestContext": {
                "accountId": "123456789012",
                "apiId": "<urlid>",
                "domainName": "<url-id>.lambda-url.us-west-2.on.aws",
                "domainPrefix": "<url-id>",
                "http": {
                    "method": "POST",
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
            "body": json.dumps({
                "item_name": "Monitor",
                "item_description": "27 inch 4K monitor",
                "item_type": "type1",
                "item_image": "https://example.com/images/monitor.png"
            }),
            "pathParameters": None,
            "isBase64Encoded": None,
            "stageVariables": None
        }

        response = lambda_handler(event, None)
        body = json.loads(response["body"])

        assert response["statusCode"] == 201
        assert body["item_name"] == "Monitor"
        assert body["message"] == "the item was created successfully"
