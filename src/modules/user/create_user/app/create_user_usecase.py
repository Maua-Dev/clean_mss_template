from uuid import UUID

from src.shared.domain.entities.user import User
from src.shared.domain.repositories.user_repository_interface import IUserRepository


class CreateUserUsecase:
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    def __call__(
        self,
        user_id: UUID,
        user_name: str,
        user_email: str,
    ) -> User:

        user = User(
            user_id=user_id,
            user_name=user_name,
            user_email=user_email,
        )
        return self.user_repo.create_user(user)
