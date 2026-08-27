from typing import Any, Optional


def generate_policy(
    principal_id: str,
    effect: str,
    method_arn: str,
    context: Optional[dict[str, Any]] = None,
) -> dict[str, Any]:
    """
    Build an API Gateway TOKEN authorizer IAM policy response.

    Args:
        principal_id: Caller principal (usually Microsoft Graph user id).
        effect: "Allow" or "Deny".
        method_arn: ARN of the method being authorized.
        context: Optional string-keyed context passed to the downstream Lambda.

    Returns:
        Authorizer response with principalId, policyDocument and optional context.
    """
    auth_response: dict[str, Any] = {"principalId": principal_id}

    if effect:
        auth_response["policyDocument"] = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Action": "execute-api:Invoke",
                    "Effect": effect,
                    "Resource": method_arn,
                }
            ],
        }

    if context:
        auth_response["context"] = context

    return auth_response
