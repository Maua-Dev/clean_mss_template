from uuid import UUID

import pytest

from src.shared.domain.entities.user import User
from src.shared.domain.enums.user_role_enum import UserRoleEnum
from src.shared.helpers.errors.domain_errors import EntityError


class Test_User:
    def test_create_user_valid(self):
        user = User(
            user_name="Dave",
            user_email="dave@example.com",
        )

        assert isinstance(user.user_id, UUID)
        assert user.user_role == UserRoleEnum.USER
        assert user.created_at > 0

    def test_create_user_admin(self):
        user = User(
            user_name="Alice",
            user_email="alice@example.com",
            user_role=UserRoleEnum.ADMIN,
        )

        assert user.user_role == UserRoleEnum.ADMIN

    def test_user_invalid_email(self):
        with pytest.raises(EntityError) as err:
            User(user_name="Dave", user_email="not-an-email")
        assert err.value.message == "Field user_email is not valid"

    def test_user_name_too_short(self):
        with pytest.raises(EntityError):
            User(user_name="D", user_email="dave@example.com")

    def test_user_invalid_role(self):
        with pytest.raises(EntityError):
            User(
                user_name="Dave",
                user_email="dave@example.com",
                user_role="SuperUser",
            )

    def test_user_frozen_created_at(self):
        user = User(
            user_name="Dave",
            user_email="dave@example.com",
            created_at=1_700_000_000,
        )

        with pytest.raises(Exception):
            user.created_at = 2

    def test_model_dump_json_mode(self):
        user = User(
            user_id=UUID("aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa"),
            user_name="Alice",
            user_email="alice@example.com",
            user_role="Admin",
            created_at=1_700_000_000,
        )
        dumped = user.model_dump(mode="json")

        assert dumped["user_id"] == "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa"
        assert dumped["user_role"] == "Admin"
        assert dumped["user_email"] == "alice@example.com"
