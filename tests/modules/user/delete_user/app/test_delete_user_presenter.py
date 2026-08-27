import os

os.environ["STAGE"] = "TEST"

from src.modules.user.delete_user.app.delete_user_presenter import lambda_handler


class Test_DeleteUserPresenter:
    def test_delete_user(self):
        event = {
            "version": "2.0",
            "rawPath": "/users/aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa",
            "headers": {},
            "queryStringParameters": None,
            "pathParameters": {"user_id": "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa"},
            "requestContext": {
                "http": {
                    "method": "DELETE",
                    "path": "/users/aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa",
                    "protocol": "HTTP/1.1",
                    "sourceIp": "1.1.1.1",
                    "userAgent": "agent",
                }
            },
            "body": None,
        }

        response = lambda_handler(event, None)
        assert response["statusCode"] == 204
        assert response["body"] in ("null", "{}", "\"\"", "")
