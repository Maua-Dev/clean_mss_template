from src.modules.user.create_user.app.create_user_viewmodel import CreateUserViewmodel
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_CreateUserViewmodel:
    def test_create_user_viewmodel(self):
        user = UserRepositoryMock().users[0]
        result = CreateUserViewmodel(user).to_dict()

        assert result["user_id"] == str(user.user_id)
        assert result["message"] == "the user was created successfully"
