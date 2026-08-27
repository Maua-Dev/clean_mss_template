import json
import os

os.environ["STAGE"] = "TEST"

from src.modules.user.auth_user.app.auth_user_presenter import lambda_handler


class Test_AuthUserPresenter:
    def test_auth_user(self):
        event = {
            "version": "2.0",
            "routeKey": "$default",
            "rawPath": "/auth-user",
            "rawQueryString": "",
            "headers": {},
            "queryStringParameters": None,
            "requestContext": {
                "http": {
                    "method": "POST",
                    "path": "/auth-user",
                    "protocol": "HTTP/1.1",
                    "sourceIp": "123.123.123.123",
                    "userAgent": "agent"
                },
                "authorizer": {
                    "user": json.dumps({
                        "sub": "dddddddd-dddd-4ddd-8ddd-dddddddddddd",
                        "mail": "dave@example.com",
                        "name": "Dave",
                    })
                }
            },
            "body": None,
        }

        response = lambda_handler(event, None)
        body = json.loads(response["body"])

        assert response["statusCode"] == 201
        assert body["user_name"] == "Dave"
        assert body["message"] == "the user was created successfully"
