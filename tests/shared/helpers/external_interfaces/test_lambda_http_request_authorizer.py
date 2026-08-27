import json

from src.shared.helpers.auth.authorizer_user import USER_FROM_AUTHORIZER_KEY
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest


class Test_LambdaHttpRequestAuthorizerUser:
    def test_injects_user_from_authorizer_into_data(self):
        user = {
            "sub": "ms-admin",
            "mail": "alice@example.com",
            "name": "Alice Admin",
        }
        event = {
            "headers": {},
            "queryStringParameters": None,
            "body": json.dumps({"item_name": "Monitor"}),
            "requestContext": {
                "http": {"method": "POST", "path": "/items"},
                "authorizer": {"user": json.dumps(user)},
            },
        }

        request = LambdaHttpRequest(data=event)

        assert request.data.get(USER_FROM_AUTHORIZER_KEY) == user
        assert request.data.get("item_name") == "Monitor"

    def test_overwrites_spoofed_body_user_from_authorizer(self):
        event = {
            "headers": {},
            "queryStringParameters": None,
            "body": json.dumps({
                USER_FROM_AUTHORIZER_KEY: {
                    "sub": "spoof",
                    "mail": "spoof@example.com",
                    "name": "Spoof",
                },
                "item_name": "Monitor",
            }),
            "requestContext": {
                "http": {"method": "POST", "path": "/items"},
                "authorizer": {
                    "user": json.dumps({
                        "sub": "ms-user",
                        "mail": "bob@example.com",
                        "name": "Bob User",
                    })
                },
            },
        }

        request = LambdaHttpRequest(data=event)

        assert request.data[USER_FROM_AUTHORIZER_KEY]["mail"] == "bob@example.com"
        assert request.data[USER_FROM_AUTHORIZER_KEY]["sub"] == "ms-user"

    def test_path_parameters_win_over_body_and_query(self):
        event = {
            "headers": {},
            "queryStringParameters": {"user_id": "from-query"},
            "pathParameters": {"user_id": "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa"},
            "body": json.dumps({"user_id": "from-body", "user_name": "Dave"}),
            "requestContext": {
                "http": {"method": "GET", "path": "/users/aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa"},
            },
        }

        request = LambdaHttpRequest(data=event)

        assert request.data["user_id"] == "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa"
        assert request.data["user_name"] == "Dave"
