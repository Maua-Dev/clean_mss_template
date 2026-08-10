from uuid import UUID

import pytest

from src.modules.item.delete_item.app.delete_item_usecase import DeleteItemUsecase
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.infra.repositories.item_repository_mock import ItemRepositoryMock


class Test_DeleteItemUsecase:
    def test_delete_item(self):
        repo = ItemRepositoryMock()
        usecase = DeleteItemUsecase(repo)
        item_id = repo.items[0].item_id

        deleted = usecase(item_id=item_id)

        assert deleted.item_id == item_id
        assert deleted.item_name == "Notebook"
        with pytest.raises(NoItemsFound):
            repo.get_item(item_id)

    def test_delete_item_not_found(self):
        repo = ItemRepositoryMock()
        usecase = DeleteItemUsecase(repo)

        with pytest.raises(NoItemsFound):
            usecase(item_id=UUID("99999999-9999-4999-8999-999999999999"))
