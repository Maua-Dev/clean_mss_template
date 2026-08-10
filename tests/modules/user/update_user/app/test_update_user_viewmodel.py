from src.modules.user.update_user.app.update_user_viewmodel import UpdateUserViewmodel
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_UpdateUserViewmodel:
    def test_update_user_viewmodel(self):
        user = UserRepositoryMock().users[0]
        result = UpdateUserViewmodel(user).to_dict()
        assert result["message"] == "the user was updated successfully"
