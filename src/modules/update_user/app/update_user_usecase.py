from uuid import UUID

from src.shared.domain.entities.user import User
from src.shared.domain.repositories.user_repository_interface import IUserRepository


class UpdateUserUsecase:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    def __call__(
        self,
        user_id: UUID,
        user_name: str,
        user_email: str,
        user_role: str,
    ) -> User:
        existing = self.repo.get_user(user_id)

        updated_user = User(
            user_id=existing.user_id,
            user_name=user_name,
            user_email=user_email,
            user_role=user_role,
            created_at=existing.created_at,
        )

        return self.repo.update_user(updated_user)
