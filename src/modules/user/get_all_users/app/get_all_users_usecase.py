from typing import List

from src.shared.domain.entities.user import User
from src.shared.domain.repositories.user_repository_interface import IUserRepository


class GetAllUsersUsecase:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    def __call__(self) -> List[User]:
        return self.repo.get_all_users()
