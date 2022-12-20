import pytest

from src.modules.update_user.app.update_user_usecase import UpdateUserUsecase
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_UpdateUserUsecase:
    def test_update_user_usecase(selfs):
        repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(repo=repo)
        updated_user = usecase(user_id=1, new_name="Bruno Guirão MPNTM")

        assert updated_user.name == "Bruno Guirão MPNTM"

    def test_update_user_usecase_wrong_user_id(selfs):
        repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(repo=repo)

        with pytest.raises(EntityError):
            usecase(user_id="1", new_name="Bruno Guirão MPNTM")

    def test_update_user_usecase_wrong_new_name(selfs):
        repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(repo=repo)

        with pytest.raises(EntityError):
            usecase(user_id=1, new_name=1)

