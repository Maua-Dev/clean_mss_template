

from src.shared.domain.entities.user import User
from src.shared.domain.enums.state_enum import STATE
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.domain_errors import EntityError


class CreateUserUsecase:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    def __call__(self, name: str, email: str) -> User:

        if not User.validate_name(name):
            raise EntityError("name")

        if not User.validate_email(email):
            raise EntityError("email")

        user = User(
            name=name,
            email=email,
            state=STATE.PENDING
        )

        return self.repo.create_user(user)
