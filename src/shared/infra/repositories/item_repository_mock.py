from typing import List
from uuid import UUID

from src.shared.domain.entities.item import Item
from src.shared.domain.enums.item_type_enum import ItemTypeEnum
from src.shared.domain.repositories.item_repository_interface import IItemRepository
from src.shared.helpers.errors.usecase_errors import DuplicatedItem, NoItemsFound


class ItemRepositoryMock(IItemRepository):
    items: List[Item]
    item_counter: int

    def __init__(self):
        self.items = [
            Item(
                item_id=UUID("11111111-1111-4111-8111-111111111111"),
                item_name="Notebook",
                item_description="Lightweight laptop for study and work",
                item_type=ItemTypeEnum.TYPE1,
                item_image="https://example.com/images/notebook.png",
                created_at=1_700_000_000,
            ),
            Item(
                item_id=UUID("22222222-2222-4222-8222-222222222222"),
                item_name="Mouse",
                item_description="Wireless mouse with silent click",
                item_type=ItemTypeEnum.TYPE2,
                item_image="https://example.com/images/mouse.png",
                created_at=1_700_000_100,
            ),
            Item(
                item_id=UUID("33333333-3333-4333-8333-333333333333"),
                item_name="Keyboard",
                item_description="Mechanical keyboard with RGB",
                item_type=None,
                item_image="https://example.com/images/keyboard.png",
                created_at=1_700_000_200,
            ),
        ]
        self.item_counter = len(self.items)

    def get_item(self, item_id: UUID) -> Item:
        for item in self.items:
            if item.item_id == item_id:
                return item
        raise NoItemsFound("item_id")

    def get_all_item(self) -> List[Item]:
        return self.items

    def get_items_by_type(self, item_type: ItemTypeEnum) -> List[Item]:
        matched = [item for item in self.items if item.item_type == item_type]
        return sorted(matched, key=lambda item: item.created_at)

    def create_item(self, new_item: Item) -> Item:
        for item in self.items:
            if item.item_id == new_item.item_id:
                raise DuplicatedItem("item_id")

        self.items.append(new_item)
        self.item_counter += 1
        return new_item

    def delete_item(self, item_id: UUID) -> Item:
        for idx, item in enumerate(self.items):
            if item.item_id == item_id:
                return self.items.pop(idx)

        raise NoItemsFound("item_id")

    def update_item(self, updated_item: Item) -> Item:
        for idx, item in enumerate(self.items):
            if item.item_id == updated_item.item_id:
                self.items[idx] = updated_item
                return updated_item

        raise NoItemsFound("item_id")

    def get_item_counter(self) -> int:
        return self.item_counter
