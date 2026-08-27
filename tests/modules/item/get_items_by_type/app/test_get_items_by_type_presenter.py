import json
import os

os.environ["STAGE"] = "TEST"

from src.modules.item.get_items_by_type.app.get_items_by_type_presenter import lambda_handler


class Test_GetItemsByTypePresenter:
    def test_get_items_by_type(self):
        event = {
            "version": "2.0",
            "rawPath": "/items/by-type",
            "headers": {},
            "queryStringParameters": {"type": "type1"},
            "pathParameters": None,
            "requestContext": {
                "http": {
                    "method": "GET",
                    "path": "/items/by-type",
                    "protocol": "HTTP/1.1",
                    "sourceIp": "1.1.1.1",
                    "userAgent": "agent",
                }
            },
            "body": None,
        }

        response = lambda_handler(event, None)
        body = json.loads(response["body"])
        assert response["statusCode"] == 200
        assert body["items"][0]["item_name"] == "Notebook"
