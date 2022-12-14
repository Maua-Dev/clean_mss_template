from src.shared.domain.entities.user import User
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.domain_errors import EntityError


class UpdateUserUsecase:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    def __call__(self, idUser: int, new_name: str) -> User:

        if type(idUser) != int:
            raise EntityError("idUser")
        
        if type(new_name) != str:
            raise EntityError("new_name")

        updated_user = self.repo.update_user(idUser=idUser, new_name=new_name)

        return updated_user
