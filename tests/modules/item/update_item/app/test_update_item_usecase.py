from uuid import UUID

import pytest

from src.modules.item.update_item.app.update_item_usecase import UpdateItemUsecase
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import ForbiddenAction, NoItemsFound
from src.shared.infra.repositories.item_repository_mock import ItemRepositoryMock
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock

_ADMIN_CLAIMS = {"sub": "ms-admin", "mail": "alice@example.com", "name": "Alice Admin"}
_USER_CLAIMS = {"sub": "ms-user", "mail": "bob@example.com", "name": "Bob User"}


class Test_UpdateItemUsecase:
    def test_update_item(self):
        item_repo = ItemRepositoryMock()
        user_repo = UserRepositoryMock()
        usecase = UpdateItemUsecase(item_repo, user_repo)
        item = item_repo.items[0]

        updated = usecase(
            item_id=item.item_id,
            item_name="Ultrabook",
            item_description="Updated description",
            item_type="type2",
            item_image="https://example.com/images/ultrabook.png",
            user_from_authorizer=_ADMIN_CLAIMS,
        )

        assert updated.item_id == item.item_id
        assert updated.item_name == "Ultrabook"
        assert updated.created_at == item.created_at
        assert item_repo.get_item(item.item_id).item_name == "Ultrabook"

    def test_update_item_forbidden_for_non_admin(self):
        item_repo = ItemRepositoryMock()
        user_repo = UserRepositoryMock()
        usecase = UpdateItemUsecase(item_repo, user_repo)

        with pytest.raises(ForbiddenAction):
            usecase(
                item_id=item_repo.items[0].item_id,
                item_name="Ultrabook",
                item_description="Updated description",
                item_type="type2",
                item_image="https://example.com/images/ultrabook.png",
                user_from_authorizer=_USER_CLAIMS,
            )

    def test_update_item_not_found(self):
        item_repo = ItemRepositoryMock()
        user_repo = UserRepositoryMock()
        usecase = UpdateItemUsecase(item_repo, user_repo)

        with pytest.raises(NoItemsFound):
            usecase(
                item_id=UUID("99999999-9999-4999-8999-999999999999"),
                item_name="Ultrabook",
                item_description="Updated description",
                item_type="type2",
                item_image="https://example.com/images/ultrabook.png",
                user_from_authorizer=_ADMIN_CLAIMS,
            )

    def test_update_item_invalid_name(self):
        item_repo = ItemRepositoryMock()
        user_repo = UserRepositoryMock()
        usecase = UpdateItemUsecase(item_repo, user_repo)

        with pytest.raises(EntityError):
            usecase(
                item_id=item_repo.items[0].item_id,
                item_name="   ",
                item_description="Updated description",
                item_type="type2",
                item_image="https://example.com/images/ultrabook.png",
                user_from_authorizer=_ADMIN_CLAIMS,
            )
