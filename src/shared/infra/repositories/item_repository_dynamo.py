from typing import List
from uuid import UUID

from boto3.dynamodb.conditions import Key

from src.shared.domain.entities.item import Item
from src.shared.domain.enums.item_type_enum import ItemTypeEnum
from src.shared.domain.repositories.item_repository_interface import IItemRepository
from src.shared.environments import Environments
from src.shared.helpers.errors.usecase_errors import DuplicatedItem, NoItemsFound
from src.shared.infra.dto.item_dynamo_dto import ItemDynamoDTO
from src.shared.infra.external.dynamo.datasources.dynamo_datasource import DynamoDatasource
from src.shared.infra.external.dynamo.dynamo_keys import (
    EntityKind,
    GSI1_NAME,
    GSI1_PK_ATTR,
    PK_ATTR,
    gsi1_partition_key,
    partition_key,
    sort_key,
)


class ItemRepositoryDynamo(IItemRepository):

    def __init__(self):
        envs = Environments.get_envs()
        self.dynamo = DynamoDatasource(
            dynamo_table_name=envs.dynamo_table_name,
            region=envs.region,
            partition_key=envs.dynamo_partition_key,
            sort_key=envs.dynamo_sort_key,
            endpoint_url=envs.dynamo_endpoint_url,
        )

    def _pk(self) -> str:
        return partition_key(kind=EntityKind.ITEM)

    def _sk(self, item_id: UUID) -> str:
        return sort_key(id=item_id, kind=EntityKind.ITEM)

    def get_item(self, item_id: UUID) -> Item:
        resp = self.dynamo.get_item(
            partition_key=self._pk(),
            sort_key=self._sk(item_id),
        )

        if resp.get("Item") is None:
            raise NoItemsFound("item_id")

        return ItemDynamoDTO.from_dynamo_to_entity(resp["Item"])

    def get_all_item(self) -> List[Item]:
        resp = self.dynamo.query(
            key_condition_expression=Key(PK_ATTR).eq(self._pk()),
        )

        return [
            ItemDynamoDTO.from_dynamo_to_entity(item)
            for item in resp.get("Items", [])
        ]

    def get_items_by_type(self, item_type: ItemTypeEnum) -> List[Item]:
        resp = self.dynamo.query(
            key_condition_expression=Key(GSI1_PK_ATTR).eq(gsi1_partition_key(item_type)),
            IndexName=GSI1_NAME,
        )

        return [
            ItemDynamoDTO.from_dynamo_to_entity(item)
            for item in resp.get("Items", [])
        ]

    def create_item(self, new_item: Item) -> Item:
        existing = self.dynamo.get_item(
            partition_key=self._pk(),
            sort_key=self._sk(new_item.item_id),
        )
        if existing.get("Item") is not None:
            raise DuplicatedItem("item_id")

        self.dynamo.put_item(
            item=ItemDynamoDTO.from_entity_to_dynamo(new_item),
            partition_key=self._pk(),
            sort_key=self._sk(new_item.item_id),
        )
        return new_item

    def delete_item(self, item_id: UUID) -> Item:
        resp = self.dynamo.delete_item(
            partition_key=self._pk(),
            sort_key=self._sk(item_id),
        )

        if "Attributes" not in resp:
            raise NoItemsFound("item_id")

        return ItemDynamoDTO.from_dynamo_to_entity(resp["Attributes"])

    def update_item(self, updated_item: Item) -> Item:
        existing = self.dynamo.get_item(
            partition_key=self._pk(),
            sort_key=self._sk(updated_item.item_id),
        )
        if existing.get("Item") is None:
            raise NoItemsFound("item_id")

        self.dynamo.put_item(
            item=ItemDynamoDTO.from_entity_to_dynamo(updated_item),
            partition_key=self._pk(),
            sort_key=self._sk(updated_item.item_id),
        )
        return updated_item

    def get_item_counter(self) -> int:
        resp = self.dynamo.query(
            key_condition_expression=Key(PK_ATTR).eq(self._pk()),
            Select="COUNT",
        )
        return resp.get("Count", 0)
