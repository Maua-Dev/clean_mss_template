from src.shared.domain.entities.user import User
from typing import List
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.usecase_errors import NoItemsFound


class GetAllUsersUsecase:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    def __call__(self) -> List[User]:
        all_users_list = self.repo.get_all_user()

        if all_users_list is None or len(all_users_list) == 0:
            return []

        return all_users_list
