import json
import os

os.environ["STAGE"] = "TEST"

from src.modules.get_all_users.app.get_all_users_presenter import lambda_handler


class Test_GetAllUsersPresenter:
    def test_get_all_users(self):
        event = {
            "version": "2.0",
            "rawPath": "/my/path",
            "headers": {},
            "queryStringParameters": None,
            "requestContext": {"http": {"method": "GET", "path": "/my/path", "protocol": "HTTP/1.1", "sourceIp": "1.1.1.1", "userAgent": "agent"}},
            "body": None,
        }

        response = lambda_handler(event, None)
        body = json.loads(response["body"])
        assert response["statusCode"] == 200
        assert len(body["all_users"]) == 3
