import json

from src.modules.get_all_users.app.get_all_users_presenter import lambda_handler


class Test_GetAllUsersPresenter:
    def test_get_all_users_presenter(self):
        expected_body = {
            "all_users": [
                {
                    'user_id': 1,
                    'name': "Bruno Soller",
                    'email': "soller@soller.com",
                    'state': 'APPROVED',
                },
                {
                    'user_id': 2,
                    'name': "Vitor Brancas",
                    'email': "brancas@brancas.com",
                    'state': 'REJECTED',
                },
                {
                    'user_id': 3,
                    'name': "João Vilas",
                    'email': "bruno@bruno.com",
                    'state': 'PENDING',
                }
            ],
            "message": "all users has been retrieved"
        }

        response = lambda_handler(event={}, context={""})

        assert response["statusCode"] == 200
        assert json.loads(response["body"]) == expected_body
