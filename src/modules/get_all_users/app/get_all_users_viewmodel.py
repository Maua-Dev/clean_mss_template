from typing import List

from src.shared.domain.entities.user import User


class GetAllUsersViewmodel:
    def __init__(self, users_list: List[User]):
        self.users_list = users_list

    def user_to_dict(self, user: User):
        return {
            'user_id': user.user_id,
            'name': user.name,
            'email': user.email,
            'state': user.state.value
        }

    def to_dict(self):
        users_dict_list: List[dict] = []

        for user in self.users_list:
            users_dict_list.append(self.user_to_dict(user))

        return {
            "all_users": users_dict_list,
            "message": "all users has been retrieved"
        }
