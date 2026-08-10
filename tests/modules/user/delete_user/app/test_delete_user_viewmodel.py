from src.modules.user.delete_user.app.delete_user_viewmodel import DeleteUserViewmodel
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_DeleteUserViewmodel:
    def test_delete_user_viewmodel(self):
        user = UserRepositoryMock().users[0]
        result = DeleteUserViewmodel(user).to_dict()
        assert result["message"] == "the user was deleted successfully"
