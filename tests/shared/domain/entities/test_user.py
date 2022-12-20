from src.shared.domain.entities.user import User
from src.shared.domain.enums.state_enum import STATE
from src.shared.helpers.errors.domain_errors import EntityError
import pytest


class Test_User:
    def test_user(self):
        User(name="VITOR", email="21.01444-2@maua.br", user_id=1, state=STATE.APPROVED)

    def test_user_name_is_none(self):
        with pytest.raises(EntityError):
            User(name=None, email="21.01444-2@maua.br", user_id=1, state=STATE.APPROVED)

    def test_user_name_is_not_str(self):
        with pytest.raises(EntityError):
            User(name=1, email="21.01444-2@maua.br", user_id=1, state=STATE.APPROVED)

    def test_user_name_is_shorter_than_min_length(self):
        with pytest.raises(EntityError):
            User(name="V", email="21.01444-2@maua.br", user_id=1, state=STATE.APPROVED)

    def test_user_email_is_none(self):
        with pytest.raises(EntityError):
            User(name="VITOR", email=None, user_id=1, state=STATE.APPROVED)

    def test_user_email_is_not_valid(self):
        with pytest.raises(EntityError):
            User(name="VITOR", email="21.01444-2maua.br", user_id=1, state=STATE.APPROVED)

    def test_user_user_id_is_not_int(self):
        with pytest.raises(EntityError):
            User(name="VITOR", email="21.01444-2@maua.br", user_id="1", state=STATE.APPROVED)

    def test_user_user_id_is_negative(self):
        with pytest.raises(EntityError):
            User(name="VITOR", email="21.01444-2@maua.br", user_id=-1, state=STATE.APPROVED)

    def test_user_state_is_not_sate_enum(self):
        with pytest.raises(EntityError):
            User(name="VITOR", email="21.01444-2@maua.br", user_id=1, state="APPROVED")
