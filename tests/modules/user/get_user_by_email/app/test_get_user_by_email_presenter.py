import json
import os

os.environ["STAGE"] = "TEST"

from src.modules.user.get_user_by_email.app.get_user_by_email_presenter import lambda_handler


class Test_GetUserByEmailPresenter:
    def test_get_user_by_email(self):
        event = {
            "version": "2.0",
            "rawPath": "/my/path",
            "headers": {},
            "queryStringParameters": {"user_email": "carol@example.com"},
            "requestContext": {"http": {"method": "GET", "path": "/my/path", "protocol": "HTTP/1.1", "sourceIp": "1.1.1.1", "userAgent": "agent"}},
            "body": None,
        }

        response = lambda_handler(event, None)
        body = json.loads(response["body"])
        assert response["statusCode"] == 200
        assert body["user_name"] == "Carol User"
