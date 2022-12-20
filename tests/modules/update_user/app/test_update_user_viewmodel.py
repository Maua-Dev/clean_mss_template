from src.modules.update_user.app.update_user_viewmodel import UpdateUserViewmodel
from src.shared.domain.entities.user import User
from src.shared.domain.enums.state_enum import STATE


class Test_UpadateUserViewmodel:
    def test_update_user_viewmodel(self):
        user = User(user_id=1, name="Test", email="teste@test.com", state=STATE.APPROVED)

        updated_useer_viewmodel = UpdateUserViewmodel(user)

        expected = {
            'user_id': 1,
            'name': "Test",
            'email': "teste@test.com",
            'state': "APPROVED",
            'message': "the user was updated successfully"
        }

        assert expected == updated_useer_viewmodel.to_dict()
