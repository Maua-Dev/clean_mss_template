import json
import os

os.environ["STAGE"] = "TEST"

from src.modules.item.update_item.app.update_item_presenter import lambda_handler


class Test_UpdateItemPresenter:
    def test_update_item(self):
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
                "item_id": "11111111-1111-4111-8111-111111111111",
                "item_name": "Ultrabook",
                "item_description": "Updated description",
                "item_type": "type2",
                "item_image": "https://example.com/images/ultrabook.png"
            }),
            "pathParameters": None,
            "isBase64Encoded": None,
            "stageVariables": None
        }

        response = lambda_handler(event, None)
        body = json.loads(response["body"])

        assert response["statusCode"] == 200
        assert body["item_name"] == "Ultrabook"
        assert body["message"] == "the item was updated successfully"
