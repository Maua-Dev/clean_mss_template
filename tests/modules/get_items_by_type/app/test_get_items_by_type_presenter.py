import json
import os

os.environ["STAGE"] = "TEST"

from src.modules.get_items_by_type.app.get_items_by_type_presenter import lambda_handler


class Test_GetItemsByTypePresenter:
    def test_get_items_by_type(self):
        event = {
            "version": "2.0",
            "rawPath": "/my/path",
            "headers": {},
            "queryStringParameters": {"item_type": "type1"},
            "requestContext": {"http": {"method": "GET", "path": "/my/path", "protocol": "HTTP/1.1", "sourceIp": "1.1.1.1", "userAgent": "agent"}},
            "body": None,
        }

        response = lambda_handler(event, None)
        body = json.loads(response["body"])
        assert response["statusCode"] == 200
        assert body["items"][0]["item_name"] == "Notebook"
