import pytest

from src.modules.item.create_item.app.create_item_usecase import CreateItemUsecase
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import ForbiddenAction
from src.shared.infra.repositories.item_repository_mock import ItemRepositoryMock
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock

_ADMIN_CLAIMS = {"sub": "ms-admin", "mail": "alice@example.com", "name": "Alice Admin"}
_USER_CLAIMS = {"sub": "ms-user", "mail": "bob@example.com", "name": "Bob User"}


class Test_CreateItemUsecase:
    def test_create_item(self):
        item_repo = ItemRepositoryMock()
        user_repo = UserRepositoryMock()
        usecase = CreateItemUsecase(item_repo, user_repo)

        item = usecase(
            item_name="Monitor",
            item_description="27 inch 4K monitor",
            item_type="type1",
            item_image="https://example.com/images/monitor.png",
            user_from_authorizer=_ADMIN_CLAIMS,
        )

        assert item_repo.items[-1] == item
        assert item.item_name == "Monitor"

    def test_create_item_forbidden_for_non_admin(self):
        item_repo = ItemRepositoryMock()
        user_repo = UserRepositoryMock()
        usecase = CreateItemUsecase(item_repo, user_repo)

        with pytest.raises(ForbiddenAction):
            usecase(
                item_name="Monitor",
                item_description="27 inch 4K monitor",
                item_type="type1",
                item_image="https://example.com/images/monitor.png",
                user_from_authorizer=_USER_CLAIMS,
            )

    def test_create_item_invalid_name(self):
        item_repo = ItemRepositoryMock()
        user_repo = UserRepositoryMock()
        usecase = CreateItemUsecase(item_repo, user_repo)

        with pytest.raises(EntityError):
            usecase(
                item_name="   ",
                item_description="27 inch 4K monitor",
                item_type="type1",
                item_image="https://example.com/images/monitor.png",
                user_from_authorizer=_ADMIN_CLAIMS,
            )

    def test_create_item_invalid_type(self):
        item_repo = ItemRepositoryMock()
        user_repo = UserRepositoryMock()
        usecase = CreateItemUsecase(item_repo, user_repo)

        with pytest.raises(EntityError):
            usecase(
                item_name="Monitor",
                item_description="27 inch 4K monitor",
                item_type="invalid",
                item_image="https://example.com/images/monitor.png",
                user_from_authorizer=_ADMIN_CLAIMS,
            )
