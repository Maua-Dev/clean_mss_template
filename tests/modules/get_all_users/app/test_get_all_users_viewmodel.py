from src.modules.get_all_users.app.get_all_users_viewmodel import GetAllUsersViewmodel, UserViewmodel
from src.shared.domain.entities.user import User
from src.shared.domain.enums.state_enum import STATE


class Test_GetAllUsersViewmodel:
    all_users_list = [
        User(user_id=1,
             name="Lucas Duez",
             email="deuzexmachina@gmail.com",
             state=STATE.APPROVED),

        User(user_id=2,
             name="Laura Blablachan",
             email="laurinha@gmail.com",
             state=STATE.APPROVED),
    ]

    def test_get_all_users_viewmodel(self):
        viewmodel = GetAllUsersViewmodel(self.all_users_list)

        expected = {
            "all_users": [
                {
                    'user_id': 1,
                    'name': "Lucas Duez",
                    'email': "deuzexmachina@gmail.com",
                    'state': 'APPROVED',
                },
                {
                    'user_id': 2,
                    'name': "Laura Blablachan",
                    'email': "laurinha@gmail.com",
                    'state': 'APPROVED',
                }
            ],
            "message": "all users has been retrieved"
        }

        response = viewmodel.to_dict()

        assert response == expected

    def test_user_viewmodel(self):
        viewmodel = UserViewmodel(
            User(user_id=2,
                 name="Laura Blablachan",
                 email="laurinha@gmail.com",
                 state=STATE.APPROVED),
)

        response = viewmodel.to_dict()

        expected = {
                    'user_id': 2,
                    'name': "Laura Blablachan",
                    'email': "laurinha@gmail.com",
                    'state': 'APPROVED',
        }

        assert response == expected


    
