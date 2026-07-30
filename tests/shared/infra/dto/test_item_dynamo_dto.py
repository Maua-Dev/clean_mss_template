from uuid import UUID

from src.shared.domain.entities.item import Item
from src.shared.domain.enums.item_type_enum import ItemTypeEnum
from src.shared.infra.dto.item_dynamo_dto import ItemDynamoDTO
from src.shared.infra.repositories.item_repository_mock import ItemRepositoryMock


class Test_ItemDynamoDTO:
    def test_from_entity_to_dynamo_with_type(self):
        item = ItemRepositoryMock().items[0]
        data = ItemDynamoDTO.from_entity_to_dynamo(item)

        assert data["pk"] == "ITEM"
        assert data["sk"] == f"ITEM#{item.item_id}"
        assert data["gsi1pk"] == "TYPE#type1"
        assert data["gsi1sk"] == f"{item.created_at:013d}"
        assert data["item_name"] == "Notebook"

    def test_from_entity_to_dynamo_without_type_is_sparse(self):
        item = ItemRepositoryMock().items[2]  # Keyboard, type None
        data = ItemDynamoDTO.from_entity_to_dynamo(item)

        assert "gsi1pk" not in data
        assert "gsi1sk" not in data

    def test_from_dynamo_to_entity_roundtrip(self):
        item = ItemRepositoryMock().items[0]
        dynamo = ItemDynamoDTO.from_entity_to_dynamo(item)
        restored = ItemDynamoDTO.from_dynamo_to_entity(dynamo)

        assert restored.item_id == item.item_id
        assert restored.item_name == item.item_name
        assert restored.item_type == ItemTypeEnum.TYPE1
        assert "pk" not in restored.model_dump()
