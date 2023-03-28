from src.shared.domain.entities.user import User
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.infra.external.observability.observability_aws import ObservabilityAWS


class GetUserUsecase:
    def __init__(self, repo: IUserRepository, observability: ObservabilityAWS):
        self.repo = repo
        self.observability = observability

    def __call__(self, user_id: int) -> User:
        self.observability.log_usecase_in()
        if type(user_id) != int:
            raise EntityError("user_id")
        user = self.repo.get_user(user_id)
        self.observability.log_usecase_out()
        return user
