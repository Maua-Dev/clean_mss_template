from src.shared.domain.entities.user import User
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.domain_errors import EntityError


class DeleteUserUsecase:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    def __call__(self, user_id: int) -> User:


        if type(user_id) != int:
            raise EntityError("user_id")

        user = self.repo.delete_user(user_id)

        return user
