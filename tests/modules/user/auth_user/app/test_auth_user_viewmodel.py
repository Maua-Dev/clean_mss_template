from src.modules.user.auth_user.app.auth_user_viewmodel import AuthUserViewmodel
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_AuthUserViewmodel:
    def test_auth_user_viewmodel_created(self):
        user = UserRepositoryMock().users[0]
        result = AuthUserViewmodel(user=user, case_number=1).to_dict()

        assert result["user_id"] == str(user.user_id)
        assert result["message"] == "the user was created successfully"

    def test_auth_user_viewmodel_retrieved(self):
        user = UserRepositoryMock().users[0]
        result = AuthUserViewmodel(user=user, case_number=0).to_dict()

        assert result["message"] == "the user was retrieved successfully"
