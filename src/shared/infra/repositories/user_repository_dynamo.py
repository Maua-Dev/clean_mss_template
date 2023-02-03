from decimal import Decimal
from typing import List

from src.shared.domain.entities.user import User
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.environments import Environments
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.infra.dto.user_dynamo_dto import UserDynamoDTO
from src.shared.infra.external.dynamo.datasources.dynamo_datasource import DynamoDatasource


class UserRepositoryDynamo(IUserRepository):

    @staticmethod
    def partition_key_format(user_id) -> str:
        return f"user#{user_id}"

    @staticmethod
    def sort_key_format(user_id: int) -> str:
        return f"#{user_id}"

    def __init__(self):
        self.dynamo = DynamoDatasource(endpoint_url=Environments.get_envs().endpoint_url,
                                       dynamo_table_name=Environments.get_envs().dynamo_table_name,
                                       region=Environments.get_envs().region,
                                       partition_key=Environments.get_envs().dynamo_partition_key,
                                       sort_key=Environments.get_envs().dynamo_sort_key)
    def get_user(self, user_id: int) -> User:
        resp = self.dynamo.get_item(partition_key=self.partition_key_format(user_id), sort_key=self.sort_key_format(user_id))

        if resp.get('Item') is None:
            raise NoItemsFound("user_id")

        user_dto = UserDynamoDTO.from_dynamo(resp["Item"])
        return user_dto.to_entity()

    def get_all_user(self) -> List[User]:
        resp = self.dynamo.get_all_items()
        users = []
        for item in resp['Items']:
            if item.get("entity") == 'user':
                users.append(UserDynamoDTO.from_dynamo(item).to_entity())

        return users


    def create_user(self, new_user: User) -> User:
        print(f"repo entered.\n Repo:{self}")
        print(self.dynamo.dynamo_table.__dict__)
        new_user.user_id = self.get_user_counter()
        print(f"nre user id: {new_user.user_id}")
        user_dto = UserDynamoDTO.from_entity(user=new_user)
        resp = self.dynamo.put_item(partition_key=self.partition_key_format(new_user.user_id),
                                    sort_key=self.sort_key_format(user_id=new_user.user_id), item=user_dto.to_dynamo(),
                                    is_decimal=True)
        return new_user

    def delete_user(self, user_id: int) -> User:
        resp = self.dynamo.delete_item(partition_key=self.partition_key_format(user_id), sort_key=self.sort_key_format(user_id))

        if "Attributes" not in resp:
            raise NoItemsFound("user_id")

        return UserDynamoDTO.from_dynamo(resp['Attributes']).to_entity()

    def update_user(self, user_id: int, new_name: str) -> User:

        user = self.get_user(user_id=user_id)

        item_to_update = {}

        if new_name:
            item_to_update['name'] = new_name
        else:
            raise NoItemsFound("Nothing to update")

        resp = self.dynamo.update_item(partition_key=self.partition_key_format(user_id), sort_key=self.sort_key_format(user_id), update_dict=item_to_update)

        return UserDynamoDTO.from_dynamo(resp['Attributes']).to_entity()

    def get_user_counter(self) -> int:

        return self.update_counter()

    def update_counter(self) -> int: #TODO fix this
        print("updating counter")
        counter = int(self.dynamo.get_item(partition_key='COUNTER', sort_key='COUNTER')['Item']['COUNTER'])
        print(f"counter: {counter}")
        resp = self.dynamo.update_item(partition_key='COUNTER', sort_key='COUNTER', update_dict={'COUNTER': Decimal(counter+1)})
        print(f"resp: {resp}")

        return int(resp['Attributes']['COUNTER'])
