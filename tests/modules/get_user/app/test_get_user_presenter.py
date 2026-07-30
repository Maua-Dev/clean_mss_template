import json
import os

os.environ["STAGE"] = "TEST"

from src.modules.get_user.app.get_user_presenter import lambda_handler


class Test_GetUserPresenter:
    def test_get_user(self):
        event = {
            "version": "2.0",
            "rawPath": "/my/path",
            "headers": {},
            "queryStringParameters": {"user_id": "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa"},
            "requestContext": {"http": {"method": "GET", "path": "/my/path", "protocol": "HTTP/1.1", "sourceIp": "1.1.1.1", "userAgent": "agent"}},
            "body": None,
        }

        response = lambda_handler(event, None)
        body = json.loads(response["body"])
        assert response["statusCode"] == 200
        assert body["user_email"] == "alice@example.com"
