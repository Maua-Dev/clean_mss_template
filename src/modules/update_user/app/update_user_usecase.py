from src.shared.domain.entities.user import User
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.domain_errors import EntityError


class UpdateUserUsecase:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    def __call__(self, user_id: int, new_name: str) -> User:

        if type(user_id) != int:
            raise EntityError("user_id")
        
        if type(new_name) != str:
            raise EntityError("new_name")

        updated_user = self.repo.update_user(user_id=user_id, new_name=new_name)

        return updated_user
