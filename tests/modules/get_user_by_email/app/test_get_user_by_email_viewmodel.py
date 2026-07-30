from src.modules.get_user_by_email.app.get_user_by_email_viewmodel import GetUserByEmailViewmodel
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_GetUserByEmailViewmodel:
    def test_get_user_by_email_viewmodel(self):
        user = UserRepositoryMock().users[0]
        result = GetUserByEmailViewmodel(user).to_dict()
        assert result["user_email"] == "alice@example.com"
