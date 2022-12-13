from src.shared.domain.entities.user import User
from src.shared.domain.enums.state_enum import STATE


class CreateUserViewmodel:
    idUser: int
    name: str
    email: str
    state: STATE

    def __init__(self, user: User):
        self.idUser = user.idUser
        self.name = user.name
        self.email = user.email
        self.state = user.state

    def to_dict(self):
        return {
            'idUser': self.idUser,
            'name': self.name,
            'email': self.email,
            'state': self.state.value,
            'message': "the user was created successfully"
        }
