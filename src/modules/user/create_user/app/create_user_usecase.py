from src.shared.domain.entities.user import User
from src.shared.domain.repositories.user_repository_interface import IUserRepository


class CreateUserUsecase:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    def __call__(
        self,
        user_name: str,
        user_email: str,
        user_role: str | None = None,
    ) -> User:
        kwargs = {
            "user_name": user_name,
            "user_email": user_email,
        }
        if user_role is not None:
            kwargs["user_role"] = user_role

        user = User(**kwargs)
        return self.repo.create_user(user)
