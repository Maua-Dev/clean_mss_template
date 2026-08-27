from src.modules.user.get_all_users.app.get_all_users_viewmodel import GetAllUsersViewmodel
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_GetAllUsersViewmodel:
    def test_get_all_users_viewmodel(self):
        user_repo = UserRepositoryMock()
        result = GetAllUsersViewmodel(user_repo.users).to_dict()
        assert len(result["all_users"]) == 3
