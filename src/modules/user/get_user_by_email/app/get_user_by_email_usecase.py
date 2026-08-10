from src.shared.domain.entities.user import User
from src.shared.domain.repositories.user_repository_interface import IUserRepository


class GetUserByEmailUsecase:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    def __call__(self, user_email: str) -> User:
        return self.repo.get_user_by_email(user_email)
