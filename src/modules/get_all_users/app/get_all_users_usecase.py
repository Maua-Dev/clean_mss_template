from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.usecase_errors import NoItemsFound


class GetAllUsersUsecase:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    def __call__(self):
        all_users_list = self.repo.get_all_user()

        if all_users_list is None or len(all_users_list) == 0:
            raise NoItemsFound("No users found")

        return all_users_list
