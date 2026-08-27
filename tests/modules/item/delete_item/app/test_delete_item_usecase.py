from uuid import UUID

import pytest

from src.modules.item.delete_item.app.delete_item_usecase import DeleteItemUsecase
from src.shared.helpers.errors.usecase_errors import ForbiddenAction, NoItemsFound
from src.shared.infra.repositories.item_repository_mock import ItemRepositoryMock
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock

_ADMIN_CLAIMS = {"sub": "ms-admin", "mail": "alice@example.com", "name": "Alice Admin"}
_USER_CLAIMS = {"sub": "ms-user", "mail": "bob@example.com", "name": "Bob User"}


class Test_DeleteItemUsecase:
    def test_delete_item(self):
        item_repo = ItemRepositoryMock()
        user_repo = UserRepositoryMock()
        usecase = DeleteItemUsecase(item_repo, user_repo)
        item_id = item_repo.items[0].item_id

        deleted = usecase(item_id=item_id, user_from_authorizer=_ADMIN_CLAIMS)

        assert deleted.item_id == item_id
        assert deleted.item_name == "Notebook"
        with pytest.raises(NoItemsFound):
            item_repo.get_item(item_id)

    def test_delete_item_forbidden_for_non_admin(self):
        item_repo = ItemRepositoryMock()
        user_repo = UserRepositoryMock()
        usecase = DeleteItemUsecase(item_repo, user_repo)

        with pytest.raises(ForbiddenAction):
            usecase(
                item_id=item_repo.items[0].item_id,
                user_from_authorizer=_USER_CLAIMS,
            )

    def test_delete_item_not_found(self):
        item_repo = ItemRepositoryMock()
        user_repo = UserRepositoryMock()
        usecase = DeleteItemUsecase(item_repo, user_repo)

        with pytest.raises(NoItemsFound):
            usecase(
                item_id=UUID("99999999-9999-4999-8999-999999999999"),
                user_from_authorizer=_ADMIN_CLAIMS,
            )
