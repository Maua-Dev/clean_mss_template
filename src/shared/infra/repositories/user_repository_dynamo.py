from decimal import Decimal
from typing import List

from src.shared.domain.entities.user import User
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.environments import Environments
from src.shared.infra.dto.user_dynamo_dto import UserDynamoDto
from src.shared.infra.external.dynamo.datasources.dynamo_datasource import DynamoDatasource


class UserRepositoryDynamo(IUserRepository):

    @staticmethod
    def partition_key_format(idUser) -> str:
        return f"user#{idUser}"

    @staticmethod
    def sort_key_format(idUser: int) -> str:
        return f"#{idUser}"

    def __init__(self):
        self.dynamo = DynamoDatasource(endpoint_url=Environments.get_envs().endpoint_url,
                                       dynamo_table_name=Environments.get_envs().dynamo_table_name,
                                       region=Environments.get_envs().region,
                                       partition_key=Environments.get_envs().dynamo_partition_key,
                                       sort_key=Environments.get_envs().dynamo_sort_key)
    def get_user(self, idUser: int) -> User:
        resp = self.dynamo.get_item(partition_key=self.partition_key_format(idUser), sort_key=self.sort_key_format(idUser))
        user_dto = UserDynamoDto.from_dynamo(resp["Item"])
        return user_dto.to_entity()

    def get_all_user(self) -> List[User]:
        pass

    def create_user(self, new_user: User) -> User:
        new_user.idUser = self.get_user_counter()
        user_dto = UserDynamoDto.from_entity(user=new_user)
        resp = self.dynamo.put_item(partition_key=self.partition_key_format(new_user.idUser),
                                    sort_key=self.sort_key_format(idUser=new_user.idUser), item=user_dto.to_dynamo(),
                                    is_decimal=True)
        return new_user

    def delete_user(self, idUser: int) -> User:
        pass

    def update_user(self, idUser: int, new_name: str) -> User:
        pass

    def get_user_counter(self) -> int:

        return self.update_counter()

    def update_counter(self) -> int: #TODO fix this
        counter = int(self.dynamo.get_item(partition_key='COUNTER', sort_key='COUNTER')['Item']['COUNTER'])
        resp = self.dynamo.update_item(partition_key='COUNTER', sort_key='COUNTER', update_dict={'COUNTER': Decimal(counter+1)})

        return int(resp['Attributes']['COUNTER'])
