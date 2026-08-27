from typing import List

from src.shared.domain.entities.user import User


class GetAllUsersViewmodel:
    def __init__(self, users_list: List[User]):
        self.users_list = users_list

    def to_dict(self):
        return {
            "all_users": [user.model_dump(mode="json") for user in self.users_list],
            "message": "all users have been retrieved"
        }
