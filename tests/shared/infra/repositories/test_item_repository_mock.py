from uuid import UUID

import pytest

from src.shared.domain.entities.item import Item
from src.shared.domain.enums.item_type_enum import ItemTypeEnum
from src.shared.helpers.errors.usecase_errors import DuplicatedItem, NoItemsFound
from src.shared.infra.repositories.item_repository_mock import ItemRepositoryMock


class Test_ItemRepositoryMock:
    def test_get_item(self):
        repo = ItemRepositoryMock()
        item = repo.get_item(UUID("11111111-1111-4111-8111-111111111111"))
        assert item.item_name == "Notebook"

    def test_get_item_not_found(self):
        repo = ItemRepositoryMock()
        with pytest.raises(NoItemsFound):
            repo.get_item(UUID("99999999-9999-4999-8999-999999999999"))

    def test_get_all_item(self):
        repo = ItemRepositoryMock()
        assert len(repo.get_all_item()) == 3

    def test_get_items_by_type(self):
        repo = ItemRepositoryMock()
        items = repo.get_items_by_type(ItemTypeEnum.TYPE1)
        assert len(items) == 1
        assert items[0].item_name == "Notebook"

    def test_create_item(self):
        repo = ItemRepositoryMock()
        new_item = Item(
            item_name="Monitor",
            item_description="4K",
            item_type=ItemTypeEnum.TYPE3,
            item_image="https://example.com/monitor.png",
        )
        created = repo.create_item(new_item)
        assert created == new_item
        assert repo.get_item_counter() == 4

    def test_create_item_duplicated(self):
        repo = ItemRepositoryMock()
        with pytest.raises(DuplicatedItem):
            repo.create_item(repo.items[0])

    def test_delete_item(self):
        repo = ItemRepositoryMock()
        item_id = repo.items[0].item_id
        deleted = repo.delete_item(item_id)
        assert deleted.item_id == item_id
        with pytest.raises(NoItemsFound):
            repo.get_item(item_id)

    def test_update_item(self):
        repo = ItemRepositoryMock()
        existing = repo.items[0]
        updated = Item(
            item_id=existing.item_id,
            item_name="Ultrabook",
            item_description=existing.item_description,
            item_type=existing.item_type,
            item_image=str(existing.item_image),
            created_at=existing.created_at,
        )
        result = repo.update_item(updated)
        assert result.item_name == "Ultrabook"
        assert repo.get_item(existing.item_id).item_name == "Ultrabook"

    def test_get_item_counter(self):
        repo = ItemRepositoryMock()
        assert repo.get_item_counter() == 3
