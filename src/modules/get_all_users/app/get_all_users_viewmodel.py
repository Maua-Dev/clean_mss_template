from typing import List

from src.shared.domain.entities.user import User


class UserViewmodel:
    def __init__(self, user: User):
        self.state = user.state
        self.email = user.email
        self.name = user.name
        self.user_id = user.user_id

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'name': self.name,
            'email': self.email,
            'state': self.state.value
        }


class GetAllUsersViewmodel:
    def __init__(self, users_list: List[User]):
        self.users_viewmodel_list = [UserViewmodel(user) for user in users_list]

    def to_dict(self):
        return {
            "all_users": [viewmodel.to_dict() for viewmodel in self.users_viewmodel_list],
            "message": "all users has been retrieved"
        }
