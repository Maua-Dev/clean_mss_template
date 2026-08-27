import json
from uuid import UUID

from src.modules.microsoft_authorizer.app.microsoft_authorizer_usecase import (
    MicrosoftAuthorizerUsecase,
)
from src.shared.domain.entities.user import User
from src.shared.domain.enums.user_role_enum import UserRoleEnum
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class FakeGraphClient:
    def __init__(self, user_data: dict):
        self.user_data = user_data
        self.last_token = None

    def get_user_profile(self, access_token: str) -> dict:
        self.last_token = access_token
        return self.user_data


class Test_MicrosoftAuthorizerUsecase:
    def setup_method(self):
        self.user_repo = UserRepositoryMock()
        self.user_repo.users[0] = User(
            user_id=UUID("aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa"),
            user_name="Alice Admin",
            user_email="alice@maua.br",
            user_role=UserRoleEnum.ADMIN,
            created_at=1_700_000_000,
        )
        self.method_arn = (
            "arn:aws:execute-api:sa-east-1:123456789012:abcdef123/dev/GET/users/aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa"
        )

    def test_allow_existing_maua_user(self):
        graph = FakeGraphClient(
            {
                "id": "ms-graph-id-1",
                "mail": "alice@maua.br",
                "displayName": "Alice",
            }
        )
        usecase = MicrosoftAuthorizerUsecase(graph, self.user_repo)

        policy = usecase("Bearer token-123", self.method_arn)

        assert policy["principalId"] == "ms-graph-id-1"
        assert policy["policyDocument"]["Statement"][0]["Effect"] == "Allow"
        context_user = json.loads(policy["context"]["user"])
        assert context_user == {
            "sub": "ms-graph-id-1",
            "mail": "alice@maua.br",
            "name": "Alice",
        }
        assert graph.last_token == "token-123"

    def test_deny_non_maua_email(self):
        graph = FakeGraphClient({"id": "x", "mail": "alice@example.com"})
        usecase = MicrosoftAuthorizerUsecase(graph, self.user_repo)

        policy = usecase("token-123", self.method_arn)

        assert policy["policyDocument"]["Statement"][0]["Effect"] == "Deny"

    def test_deny_when_user_not_in_db(self):
        graph = FakeGraphClient({"id": "x", "mail": "newuser@maua.br"})
        usecase = MicrosoftAuthorizerUsecase(graph, self.user_repo)

        policy = usecase("token-123", self.method_arn)

        assert policy["policyDocument"]["Statement"][0]["Effect"] == "Deny"

    def test_allow_onboarding_route_without_db_user(self):
        graph = FakeGraphClient(
            {
                "id": "ms-graph-id-2",
                "mail": "newuser@maua.br",
            }
        )
        usecase = MicrosoftAuthorizerUsecase(graph, self.user_repo)
        method_arn = (
            "arn:aws:execute-api:sa-east-1:123456789012:abcdef123/dev/POST/auth"
        )

        policy = usecase("Bearer token-123", method_arn)

        assert policy["policyDocument"]["Statement"][0]["Effect"] == "Allow"
        assert policy["principalId"] == "ms-graph-id-2"

    def test_fallback_to_user_principal_name(self):
        graph = FakeGraphClient(
            {
                "id": "ms-graph-id-3",
                "mail": None,
                "userPrincipalName": "alice@maua.br",
            }
        )
        usecase = MicrosoftAuthorizerUsecase(graph, self.user_repo)

        policy = usecase("token-123", self.method_arn)

        assert policy["policyDocument"]["Statement"][0]["Effect"] == "Allow"
