from src.modules.create_user.app.create_user_viewmodel import CreateUserViewmodel
from src.shared.domain.entities.user import User
from src.shared.domain.enums.state_enum import STATE


class Test_CreateUserViewModel:
    def test_create_user_viewmodel(self):
        user = User(
            idUser=1,
            name="Vitor Soller",
            email="vitinho@hype.com",
            state=STATE.APPROVED
        )
        userViewmodel = CreateUserViewmodel(user=user).to_dict()

        expected = {'idUser': 1,
                    'name': 'Vitor Soller',
                    'email': 'vitinho@hype.com',
                    'state': 'APPROVED',
                    'message': 'the user was retrieved successfully'}

        assert expected == userViewmodel
