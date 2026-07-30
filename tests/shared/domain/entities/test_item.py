from uuid import UUID

import pytest

from src.shared.domain.entities.item import Item
from src.shared.domain.enums.item_type_enum import ItemTypeEnum
from src.shared.helpers.errors.domain_errors import EntityError


class Test_Item:
    def test_create_item_valid(self):
        item = Item(
            item_name="Monitor",
            item_description="4K monitor",
            item_type=ItemTypeEnum.TYPE1,
            item_image="https://example.com/monitor.png",
        )

        assert isinstance(item.item_id, UUID)
        assert item.item_name == "Monitor"
        assert item.item_type == ItemTypeEnum.TYPE1
        assert item.created_at > 0

    def test_create_item_optional_type(self):
        item = Item(
            item_name="Cable",
            item_description="USB-C cable",
            item_image="https://example.com/cable.png",
        )

        assert item.item_type is None

    def test_item_blank_name_raises_entity_error(self):
        with pytest.raises(EntityError) as err:
            Item(
                item_name="   ",
                item_description="desc",
                item_image="https://example.com/a.png",
            )
        assert err.value.message == "Field item_name is not valid"

    def test_item_invalid_image_raises_entity_error(self):
        with pytest.raises(EntityError) as err:
            Item(
                item_name="Monitor",
                item_description="desc",
                item_image="not-a-url",
            )
        assert err.value.message == "Field item_image is not valid"

    def test_item_name_too_long(self):
        with pytest.raises(EntityError):
            Item(
                item_name="x" * 31,
                item_description="desc",
                item_image="https://example.com/a.png",
            )

    def test_item_frozen_fields(self):
        item = Item(
            item_name="Monitor",
            item_description="desc",
            item_image="https://example.com/a.png",
            created_at=1_700_000_000,
        )

        with pytest.raises(Exception):
            item.created_at = 1

    def test_model_dump_json_mode(self):
        item = Item(
            item_id=UUID("11111111-1111-4111-8111-111111111111"),
            item_name="Monitor",
            item_description="desc",
            item_type="type1",
            item_image="https://example.com/a.png",
            created_at=1_700_000_000,
        )
        dumped = item.model_dump(mode="json")

        assert dumped["item_id"] == "11111111-1111-4111-8111-111111111111"
        assert dumped["item_type"] == "type1"
        assert isinstance(dumped["item_image"], str)
