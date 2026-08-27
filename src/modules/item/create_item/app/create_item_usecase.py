from src.shared.domain.entities.item import Item
from src.shared.domain.enums.user_role_enum import UserRoleEnum
from src.shared.domain.repositories.item_repository_interface import IItemRepository
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.usecase_errors import ForbiddenAction, NoUsersFound


class CreateItemUsecase:
    def __init__(self, item_repo: IItemRepository, user_repo: IUserRepository):
        self.item_repo = item_repo
        self.user_repo = user_repo

    def __call__(
        self,
        item_name: str,
        item_description: str,
        item_type: str,
        item_image: str,
        user_from_authorizer: dict,
    ) -> Item:
        mail = (user_from_authorizer or {}).get("mail")
        if not mail:
            raise ForbiddenAction("user")

        try:
            user = self.user_repo.get_user_by_email(mail)
        except NoUsersFound:
            raise ForbiddenAction("user")

        if user.user_role != UserRoleEnum.ADMIN:
            raise ForbiddenAction("user")

        item = Item(
            item_name=item_name,
            item_description=item_description,
            item_type=item_type,
            item_image=item_image
        )

        return self.item_repo.create_item(item)
