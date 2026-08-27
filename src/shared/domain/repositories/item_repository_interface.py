from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from src.shared.domain.entities.item import Item
from src.shared.domain.enums.item_type_enum import ItemTypeEnum


class IItemRepository(ABC):

    @abstractmethod
    def get_item(self, item_id: UUID) -> Item:
        """Retrieve an item by its unique identifier.

        Args:
            item_id: UUID of the item to retrieve.

        Returns:
            The item associated with the given UUID.

        Raises:
            NoItemsFound: If no item exists with the given UUID.
        """
        pass
   

    @abstractmethod
    def get_all_item(self) -> List[Item]:
        """Retrieve all stored items.

        Returns:
            A list containing all items. The list is empty when no items exist.
        """
        pass

    @abstractmethod
    def get_items_by_type(self, item_type: ItemTypeEnum) -> List[Item]:
        """Retrieve items filtered by type, ordered by created_at ascending.

        Access pattern backed by GSI ItemTypeIndex (gsi1pk / gsi1sk).
        Items without item_type are not returned (sparse index).

        Args:
            item_type: Item type to filter by.

        Returns:
            Matching items ordered by creation time.
        """
        pass

    @abstractmethod
    def create_item(self, new_item: Item) -> Item:
        """Persist a new item.

        Args:
            new_item: Item to persist.

        Returns:
            The persisted item.

        Raises:
            DuplicatedItem: If an item with the same identifier already exists.
        """
        pass

    @abstractmethod
    def delete_item(self, item_id: UUID) -> Item:
        """Delete an item by its unique identifier.

        Args:
            item_id: UUID of the item to delete.

        Returns:
            The deleted item.

        Raises:
            NoItemsFound: If no item exists with the given UUID.
        """
        pass

    @abstractmethod
    def update_item(self, updated_item: Item) -> Item:
        """Replace the stored data for an existing item.

        Args:
            updated_item: Item containing the identifier and updated data.

        Returns:
            The updated item.

        Raises:
            NoItemsFound: If the item to update does not exist.
        """
        pass

    @abstractmethod
    def get_item_counter(self) -> int:
        """Return the total number of items ever created.

        Returns:
            The cumulative number of created items.
        """
        pass
