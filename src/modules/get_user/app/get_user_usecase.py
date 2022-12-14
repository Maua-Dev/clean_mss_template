from src.shared.domain.entities.user import User
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.domain_errors import EntityError


class GetUserUsecase:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    def __call__(self, idUser: int) -> User:

        if type(idUser) != int:
            raise EntityError("idUser")

        return self.repo.get_user(idUser)
