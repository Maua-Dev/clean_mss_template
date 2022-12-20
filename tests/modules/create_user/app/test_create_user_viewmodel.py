from src.modules.create_user.app.create_user_viewmodel import CreateUserViewmodel
from src.shared.domain.entities.user import User
from src.shared.domain.enums.state_enum import STATE


class Test_CreateUserViewModel:
    def test_create_user_viewmodel(self):
        user = User(
            user_id=1,
            name="Vitor Soller",
            email="vitinho@hype.com",
            state=STATE.APPROVED
        )
        userViewmodel = CreateUserViewmodel(user=user).to_dict()

        expected = {'user_id': 1,
                    'name': 'Vitor Soller',
                    'email': 'vitinho@hype.com',
                    'state': 'APPROVED',
                    'message': 'the user was created successfully'}

        assert expected == userViewmodel
