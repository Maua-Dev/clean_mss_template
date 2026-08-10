from src.shared.domain.entities.user import User


class CreateUserViewmodel:
    def __init__(self, user: User):
        self.user = user

    def to_dict(self):
        user_dict = self.user.model_dump(mode="json")
        user_dict["message"] = "the user was created successfully"
        return user_dict
