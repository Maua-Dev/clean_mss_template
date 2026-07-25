from src.shared.domain.entities.item import Item
from src.shared.infra.external.dynamo.dynamo_keys import (
    EntityKind,
    build_gsi1_attributes,
    partition_key,
    sort_key,
    strip_keys,
)


class ItemDynamoDTO:

    @staticmethod
    def from_entity_to_dynamo(item: Item) -> dict:
        """
        Converts an Item entity to a dictionary compatible with DynamoDB.

        Includes base keys (pk/sk) and sparse GSI1 attributes (gsi1pk/gsi1sk)
        when item_type is set.

        Args:
            item: The Item entity to serialize.

        Returns:
            Dict as expected by DynamoDB put_item.
        """
        return {
            **item.model_dump(mode="json"),
            "pk": partition_key(kind=EntityKind.ITEM),
            "sk": sort_key(item_id=item.item_id, kind=EntityKind.ITEM),
            **build_gsi1_attributes(item.item_type, item.created_at),
        }

    @staticmethod
    def from_dynamo_to_entity(item_data: dict) -> Item:
        """
        Converts a DynamoDB item dict into an Item entity.

        Args:
            item_data: Dictionary from DynamoDB.

        Returns:
            Item entity with storage keys removed.
        """
        return Item.model_validate(obj=strip_keys(item_data))
