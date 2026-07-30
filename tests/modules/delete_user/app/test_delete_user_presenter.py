import json
import os

os.environ["STAGE"] = "TEST"

from src.modules.delete_user.app.delete_user_presenter import lambda_handler


class Test_DeleteUserPresenter:
    def test_delete_user(self):
        event = {
            "version": "2.0",
            "rawPath": "/my/path",
            "headers": {},
            "queryStringParameters": None,
            "requestContext": {"http": {"method": "POST", "path": "/my/path", "protocol": "HTTP/1.1", "sourceIp": "1.1.1.1", "userAgent": "agent"}},
            "body": '{"user_id":"aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa"}',
        }

        response = lambda_handler(event, None)
        assert response["statusCode"] == 200
        assert json.loads(response["body"])["user_name"] == "Alice Admin"
