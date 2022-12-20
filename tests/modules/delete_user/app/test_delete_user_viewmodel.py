from src.modules.delete_user.app.delete_user_viewmodel import DeleteUserViewmodel
from src.shared.domain.entities.user import User
from src.shared.domain.enums.state_enum import STATE


class Test_DeleteUserViewmodel:
    def test_delete_user_viewmodel(self):
        user = User(
            user_id=1,
            name="Vitinho da Silva",
            email="21.01444-2@maua.br",
            state=STATE.APPROVED)

        delete_user_viewmodel = DeleteUserViewmodel(user)

        expected = {
                    'user_id': 1,
                    'name': 'Vitinho da Silva',
                    'email': '21.01444-2@maua.br',
                    'state': 'APPROVED',
                    'message': 'the user was deleted successfully'}

        assert expected == delete_user_viewmodel.to_dict()
