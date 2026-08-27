import json
import os

os.environ["STAGE"] = "TEST"

from src.modules.user.create_user.app.create_user_presenter import lambda_handler


class Test_CreateUserPresenter:
    def test_create_user(self):
        event = {
            "version": "2.0",
            "routeKey": "$default",
            "rawPath": "/my/path",
            "rawQueryString": "",
            "headers": {},
            "queryStringParameters": None,
            "requestContext": {
                "http": {
                    "method": "POST",
                    "path": "/my/path",
                    "protocol": "HTTP/1.1",
                    "sourceIp": "123.123.123.123",
                    "userAgent": "agent"
                }
            },
            "body": json.dumps({
                "user_id": "aaaaaaaa-bbbb-4ccc-8ddd-eeeeeeeeeeee",
                "user_name": "Dave",
                "user_email": "dave@example.com",
            }),
        }

        response = lambda_handler(event, None)
        body = json.loads(response["body"])

        assert response["statusCode"] == 201
        assert body["user_name"] == "Dave"
