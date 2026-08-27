import json
import os

os.environ["STAGE"] = "TEST"

from src.modules.user.update_user.app.update_user_presenter import lambda_handler


class Test_UpdateUserPresenter:
    def test_update_user(self):
        event = {
            "version": "2.0",
            "rawPath": "/users/aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa",
            "headers": {},
            "queryStringParameters": None,
            "pathParameters": {"user_id": "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa"},
            "requestContext": {
                "http": {
                    "method": "PUT",
                    "path": "/users/aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa",
                    "protocol": "HTTP/1.1",
                    "sourceIp": "1.1.1.1",
                    "userAgent": "agent",
                }
            },
            "body": json.dumps({
                "user_name": "Alice Updated",
                "user_email": "alice.updated@example.com",
                "user_role": "Admin",
            }),
        }

        response = lambda_handler(event, None)
        assert response["statusCode"] == 200
        assert json.loads(response["body"])["user_name"] == "Alice Updated"
