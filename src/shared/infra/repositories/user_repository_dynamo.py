from typing import List
from uuid import UUID

from boto3.dynamodb.conditions import Key
from pydantic import EmailStr

from src.shared.domain.entities.user import User
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.environments import Environments
from src.shared.helpers.errors.usecase_errors import DuplicatedUser, NoUsersFound
from src.shared.infra.dto.user_dynamo_dto import UserDynamoDTO
from src.shared.infra.external.dynamo.datasources.dynamo_datasource import DynamoDatasource
from src.shared.infra.external.dynamo.dynamo_keys import (
    EntityKind,
    GSI2_NAME,
    GSI2_PK_ATTR,
    PK_ATTR,
    gsi2_partition_key,
    partition_key,
    sort_key,
)


class UserRepositoryDynamo(IUserRepository):

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
        return partition_key(kind=EntityKind.USER)

    def _sk(self, user_id: UUID) -> str:
        return sort_key(id=user_id, kind=EntityKind.USER)

    def get_user(self, user_id: UUID) -> User:
        resp = self.dynamo.get_item(
            partition_key=self._pk(),
            sort_key=self._sk(user_id),
        )

        if resp.get("Item") is None:
            raise NoUsersFound("user_id")

        return UserDynamoDTO.from_dynamo_to_entity(resp["Item"])

    def get_user_by_email(self, user_email: EmailStr) -> User:
        resp = self.dynamo.query(
            key_condition_expression=Key(GSI2_PK_ATTR).eq(gsi2_partition_key(user_email)),
            IndexName=GSI2_NAME,
        )

        items = resp.get("Items", [])
        if not items:
            raise NoUsersFound("user_email")

        return UserDynamoDTO.from_dynamo_to_entity(items[0])

    def get_all_users(self) -> List[User]:
        resp = self.dynamo.query(
            key_condition_expression=Key(PK_ATTR).eq(self._pk()),
        )

        return [
            UserDynamoDTO.from_dynamo_to_entity(user)
            for user in resp.get("Items", [])
        ]

    def create_user(self, new_user: User) -> User:
        existing = self.dynamo.get_item(
            partition_key=self._pk(),
            sort_key=self._sk(new_user.user_id),
        )
        if existing.get("Item") is not None:
            raise DuplicatedUser("user_id")

        # email uniqueness via GSI2
        email_resp = self.dynamo.query(
            key_condition_expression=Key(GSI2_PK_ATTR).eq(
                gsi2_partition_key(new_user.user_email)
            ),
            IndexName=GSI2_NAME,
            Select="COUNT",
        )
        if email_resp.get("Count", 0) > 0:
            raise DuplicatedUser("user_email")

        self.dynamo.put_item(
            item=UserDynamoDTO.from_entity_to_dynamo(new_user),
            partition_key=self._pk(),
            sort_key=self._sk(new_user.user_id),
        )
        return new_user

    def delete_user(self, user_id: UUID) -> User:
        resp = self.dynamo.delete_item(
            partition_key=self._pk(),
            sort_key=self._sk(user_id),
        )

        if "Attributes" not in resp:
            raise NoUsersFound("user_id")

        return UserDynamoDTO.from_dynamo_to_entity(resp["Attributes"])

    def update_user(self, updated_user: User) -> User:
        existing = self.dynamo.get_item(
            partition_key=self._pk(),
            sort_key=self._sk(updated_user.user_id),
        )
        if existing.get("Item") is None:
            raise NoUsersFound("user_id")

        self.dynamo.put_item(
            item=UserDynamoDTO.from_entity_to_dynamo(updated_user),
            partition_key=self._pk(),
            sort_key=self._sk(updated_user.user_id),
        )
        return updated_user

    def reallocate_user(self, updated_user: User) -> User:
        existing = self.get_user_by_email(updated_user.user_email)

        if existing.user_id != updated_user.user_id:
            conflict = self.dynamo.get_item(
                partition_key=self._pk(),
                sort_key=self._sk(updated_user.user_id),
            )
            if conflict.get("Item") is not None:
                raise DuplicatedUser("user_id")

            self.delete_user(existing.user_id)

        self.dynamo.put_item(
            item=UserDynamoDTO.from_entity_to_dynamo(updated_user),
            partition_key=self._pk(),
            sort_key=self._sk(updated_user.user_id),
        )
        return updated_user

    def get_user_counter(self) -> int:
        resp = self.dynamo.query(
            key_condition_expression=Key(PK_ATTR).eq(self._pk()),
            Select="COUNT",
        )
        return resp.get("Count", 0)
