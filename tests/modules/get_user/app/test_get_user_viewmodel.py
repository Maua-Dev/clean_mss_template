from src.modules.get_user.app.get_user_viewmodel import GetUserViewmodel
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_GetUserViewmodel:
    def test_get_user_viewmodel(self):
        user = UserRepositoryMock().users[0]
        result = GetUserViewmodel(user).to_dict()
        assert result["user_name"] == "Alice Admin"
