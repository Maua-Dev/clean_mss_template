import os

import pytest

from src.shared.helpers.errors.usecase_errors import DuplicatedUser, NoUsersFound
from src.shared.infra.repositories.user_repository_dynamo import UserRepositoryDynamo
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_UserRepositoryDynamo:

    @pytest.mark.skip(reason="Needs dynamoDB")
    def test_create_user(self):
        os.environ["STAGE"] = "TEST"

        user_repository = UserRepositoryDynamo()
        user_repository_mock = UserRepositoryMock()
        resp = user_repository.create_user(user_repository_mock.users[0])

        assert user_repository_mock.users[0].user_name == resp.user_name
        assert user_repository_mock.users[0].user_id == resp.user_id

    @pytest.mark.skip(reason="Needs dynamoDB")
    def test_get_user(self):
        os.environ["STAGE"] = "TEST"

        user_repository = UserRepositoryDynamo()
        user_repository_mock = UserRepositoryMock()
        user = user_repository_mock.users[0]

        resp = user_repository.get_user(user.user_id)

        assert resp.user_id == user.user_id
        assert resp.user_name == user.user_name

    @pytest.mark.skip(reason="Needs dynamoDB")
    def test_get_user_by_email(self):
        os.environ["STAGE"] = "TEST"

        user_repository = UserRepositoryDynamo()
        user_repository_mock = UserRepositoryMock()
        user = user_repository_mock.users[1]

        resp = user_repository.get_user_by_email(user.user_email)

        assert resp.user_email == user.user_email
        assert resp.user_name == user.user_name

    @pytest.mark.skip(reason="Needs dynamoDB")
    def test_get_all_users(self):
        os.environ["STAGE"] = "TEST"

        user_repository = UserRepositoryDynamo()
        user_repository_mock = UserRepositoryMock()

        resp = user_repository.get_all_users()

        assert len(resp) >= 3

    @pytest.mark.skip(reason="Needs dynamoDB")
    def test_update_user(self):
        os.environ["STAGE"] = "TEST"

        user_repository = UserRepositoryDynamo()
        user_repository_mock = UserRepositoryMock()
        user = user_repository_mock.users[0]

        updated = user.model_copy(update={"user_name": "Alice Updated"})
        resp = user_repository.update_user(updated)

        assert resp.user_name == "Alice Updated"
        assert user_repository.get_user(user.user_id).user_name == "Alice Updated"

    @pytest.mark.skip(reason="Needs dynamoDB")
    def test_delete_user(self):
        os.environ["STAGE"] = "TEST"

        user_repository = UserRepositoryDynamo()
        user_repository_mock = UserRepositoryMock()
        user = user_repository_mock.users[2]

        resp = user_repository.delete_user(user.user_id)

        assert resp.user_id == user.user_id
        with pytest.raises(NoUsersFound):
            user_repository.get_user(user.user_id)

    @pytest.mark.skip(reason="Needs dynamoDB")
    def test_get_user_counter(self):
        os.environ["STAGE"] = "TEST"

        user_repository = UserRepositoryDynamo()
        user_repository_mock = UserRepositoryMock()

        assert user_repository.get_user_counter() >= 3
