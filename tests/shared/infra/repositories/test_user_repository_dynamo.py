import os

import pytest

from src.shared.infra.repositories.user_repository_dynamo import UserRepositoryDynamo
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_UserRepositoryDynamo:
    @pytest.mark.skip(reason="Needs dynamoDB")
    def test_create_user(self):
        os.environ["STAGE"] = "TEST"

        user_repository = UserRepositoryDynamo()
        user_repository_mock = UserRepositoryMock()
        resp = user_repository.create_user(user_repository_mock.users[0])

        assert True

    # @pytest.mark.skip(reason="Needs dynamoDB")
    def test_get_user(self):
        os.environ["STAGE"] = "TEST"

        user_repository = UserRepositoryDynamo()
        user_repository_mock = UserRepositoryMock()
        resp = user_repository.get_user(1)

        assert user_repository_mock.users[0].name == resp.name
        assert True
