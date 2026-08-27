from uuid import UUID

from src.shared.domain.entities.user import User
from src.shared.domain.repositories.user_repository_interface import IUserRepository


class DeleteUserUsecase:
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    def __call__(self, user_id: UUID) -> User:
        return self.user_repo.delete_user(user_id)
