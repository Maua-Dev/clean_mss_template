from uuid import UUID

from src.shared.domain.entities.user import User
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.usecase_errors import NoUsersFound


class AuthUserUsecase:
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    def __call__(
        self,
        user_id: UUID,
        user_name: str,
        user_email: str,
    ) -> tuple[User, int]:
        try:
            existing = self.user_repo.get_user_by_email(user_email)
        except NoUsersFound:
            created = self.user_repo.create_user(
                User(
                    user_id=user_id,
                    user_name=user_name,
                    user_email=user_email,
                )
            )
            return created, 1

        substituted = User(
            user_id=user_id,
            user_name=user_name,
            user_email=user_email,
            user_role=existing.user_role,
            created_at=existing.created_at,
        )
        updated = self.user_repo.reallocate_user(substituted)
        return updated, 0
