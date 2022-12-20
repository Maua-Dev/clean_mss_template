from src.modules.get_user.app.get_user_viewmodel import GetUserViewmodel
from src.shared.domain.entities.user import User
from src.shared.domain.enums.state_enum import STATE


class Test_GetUserViewModel:
    def test_get_user_viewmodel(self):
        user = User(
            user_id=1,
            name="Vitor Soller",
            email="vitinho@hype.com",
            state=STATE.APPROVED
        )
        userViewmodel = GetUserViewmodel(user=user).to_dict()

        expected = {'user_id': 1,
                    'name': 'Vitor Soller',
                    'email': 'vitinho@hype.com',
                    'state': 'APPROVED',
                    'message': 'the user was retrieved successfully'}

        assert expected == userViewmodel
