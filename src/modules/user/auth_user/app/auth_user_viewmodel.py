from src.shared.domain.entities.user import User


class AuthUserViewmodel:
    def __init__(self, user: User, case_number: int):
        self.user = user
        self.case_number = case_number

    def to_dict(self):
        user_dict = self.user.model_dump(mode="json")
        if self.case_number == 1:
            user_dict["message"] = "the user was created successfully"
        else:
            user_dict["message"] = "the user was retrieved successfully"
        return user_dict
