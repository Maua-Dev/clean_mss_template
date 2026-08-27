from src.shared.helpers.auth.iam_policy import generate_policy


class Test_GeneratePolicy:
    def test_allow_policy(self):
        policy = generate_policy("principal-1", "Allow", "arn:aws:execute-api:sa-east-1:123:api/GET/users")

        assert policy["principalId"] == "principal-1"
        assert policy["policyDocument"]["Statement"][0]["Effect"] == "Allow"
        assert "context" not in policy

    def test_deny_policy_with_context(self):
        policy = generate_policy(
            "user",
            "Deny",
            "arn:aws:execute-api:*",
            context={"user": "{}"},
        )

        assert policy["policyDocument"]["Statement"][0]["Effect"] == "Deny"
        assert policy["context"]["user"] == "{}"
