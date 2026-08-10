import os

from src.modules.microsoft_authorizer.app.microsoft_authorizer_usecase import (
    MicrosoftAuthorizerUsecase,
)
from src.shared.environments import Environments
from src.shared.helpers.auth.iam_policy import generate_policy
from src.shared.helpers.observability.wrap_handler import observed_handler
from src.shared.infra.external.microsoft.graph_client import MicrosoftGraphClient

_DEFAULT_GRAPH_ENDPOINT = "https://graph.microsoft.com/v1.0/me"


def _build_usecase() -> MicrosoftAuthorizerUsecase:
    graph_endpoint = (
        os.environ.get("GRAPH_MICROSOFT_ENDPOINT")
        or os.environ.get("MS_GRAPH_ENDPOINT")
        or _DEFAULT_GRAPH_ENDPOINT
    )
    return MicrosoftAuthorizerUsecase(
        graph_client=MicrosoftGraphClient(graph_endpoint=graph_endpoint),
        user_repo=Environments.get_user_repo()(),
    )


@observed_handler("microsoft_authorizer")
def lambda_handler(event, context):
    """
    API Gateway TOKEN authorizer.

    Validates the Bearer token against Microsoft Graph, enforces @maua.br,
    and (except onboarding routes) checks that the user exists in our DB.
    """
    method_arn = event.get("methodArn", "*")

    try:
        authorization_token = event["authorizationToken"]
        usecase = _build_usecase()
        return usecase(
            authorization_token=authorization_token,
            method_arn=method_arn,
        )
    except Exception as err:
        print(f"Microsoft authorizer error: {err}")
        return generate_policy("user", "Deny", method_arn)
