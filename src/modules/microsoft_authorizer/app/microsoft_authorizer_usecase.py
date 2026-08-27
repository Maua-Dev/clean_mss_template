import re

from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.auth.authorizer_user import build_authorizer_user_context
from src.shared.helpers.auth.iam_policy import generate_policy
from src.shared.helpers.errors.usecase_errors import NoUsersFound
from src.shared.infra.external.microsoft.graph_client import MicrosoftGraphClient

# Routes where the user may not exist in our DB yet (first login / self-registration).
_ONBOARDING_PATH_MARKERS = ("/auth",)

_MAUA_EMAIL_REGEX = re.compile(r"^[^@\s]+@maua\.br$", re.IGNORECASE)


class MicrosoftAuthorizerUsecase:
    def __init__(
        self,
        graph_client: MicrosoftGraphClient,
        user_repo: IUserRepository,
    ):
        self.graph_client = graph_client
        self.user_repo = user_repo

    def __call__(self, authorization_token: str, method_arn: str) -> dict:
        token = authorization_token.replace("Bearer ", "", 1).strip()
        profile = self.graph_client.get_user_profile(token)

        sub = str(profile.get("id") or "").strip()
        mail = self._extract_email(profile)
        name = str(profile.get("displayName") or profile.get("name") or "").strip()

        if not sub or not mail or not _MAUA_EMAIL_REGEX.match(mail):
            return generate_policy("user", "Deny", method_arn)

        if not self._is_onboarding_route(method_arn):
            try:
                self.user_repo.get_user_by_email(mail)
            except NoUsersFound:
                return generate_policy("user", "Deny", method_arn)

        # context só com claims Microsoft → LambdaHttpRequest.data["user_from_authorizer"]
        return generate_policy(
            sub,
            "Allow",
            method_arn,
            build_authorizer_user_context(sub=sub, mail=mail, name=name),
        )

    @staticmethod
    def _extract_email(user_data: dict) -> str:
        # Graph may return mail empty; UPN is a common fallback for org accounts.
        return (user_data.get("mail") or user_data.get("userPrincipalName") or "").strip()

    @staticmethod
    def _is_onboarding_route(method_arn: str) -> bool:
        return any(marker in method_arn for marker in _ONBOARDING_PATH_MARKERS)
