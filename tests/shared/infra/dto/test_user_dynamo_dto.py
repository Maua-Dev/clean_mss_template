from decimal import Decimal

from src.shared.domain.entities.user import User
from src.shared.domain.enums.state_enum import STATE
from src.shared.infra.dto.user_dynamo_dto import UserDynamoDTO
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_UserDynamoDto:
    def test_from_entity(self):
        repo = UserRepositoryMock()

        user_dto = UserDynamoDTO.from_entity(user=repo.users[0])

        expected_selfie_dto = UserDynamoDTO(
            name=repo.users[0].name,
            email=repo.users[0].email,
            user_id=repo.users[0].user_id,
            state=repo.users[0].state
        )

        assert user_dto == expected_selfie_dto

    def test_to_dynamo(self):
        repo = UserRepositoryMock()

        user_dto = UserDynamoDTO(
            name=repo.users[0].name,
            email=repo.users[0].email,
            user_id=repo.users[0].user_id,
            state=repo.users[0].state
        )

        user_dynamo = user_dto.to_dynamo()

        expected_dict = {
            "entity": "user",
            "name": repo.users[0].name,
            "email": repo.users[0].email,
            "user_id": repo.users[0].user_id,
            "state": repo.users[0].state.value
        }

        assert user_dto.to_dynamo() == expected_dict

    def test_from_dynamo(self):
        dynamo_dict = {'Item': {'user_id': Decimal('1'),
                                'name': 'Bruno Soller',
                                'SK': '#1',
                                'state': 'APPROVED',
                                'PK': 'user#1',
                                'entity': 'user',
                                'email': 'soller@soller.com'},
                       'ResponseMetadata': {'RequestId': 'aa6a5e5e-943f-4452-8c1f-4e5441ee6042',
                                            'HTTPStatusCode': 200,
                                            'HTTPHeaders': {'date': 'Fri, 16 Dec 2022 15:40:29 GMT',
                                                            'content-type': 'application/x-amz-json-1.0',
                                                            'x-amz-crc32': '3909675734',
                                                            'x-amzn-requestid': 'aa6a5e5e-943f-4452-8c1f-4e5441ee6042',
                                                            'content-length': '174',
                                                            'server': 'Jetty(9.4.48.v20220622)'},
                                            'RetryAttempts': 0}}

        user_dto = UserDynamoDTO.from_dynamo(user_data=dynamo_dict["Item"])

        expected_user_dto = UserDynamoDTO(
            name="Bruno Soller",
            email='soller@soller.com',
            user_id=1,
            state=STATE.APPROVED
        )

        assert user_dto == expected_user_dto

    def test_to_entity(self):
        repo = UserRepositoryMock()

        user_dto = UserDynamoDTO(
            name=repo.users[0].name,
            email=repo.users[0].email,
            user_id=repo.users[0].user_id,
            state=repo.users[0].state
        )

        user = user_dto.to_entity()

        assert user.name == repo.users[0].name
        assert user.email == repo.users[0].email
        assert user.user_id == repo.users[0].user_id
        assert user.state == repo.users[0].state

    def test_from_dynamo_to_entity(self):
        dynamo_item = {'Item': {'user_id': Decimal('1'),
                                'name': 'Bruno Soller',
                                'SK': '#1',
                                'state': 'APPROVED',
                                'PK': 'user#1',
                                'entity': 'user',
                                'email': 'soller@soller.com'}}

        user_dto = UserDynamoDTO.from_dynamo(user_data=dynamo_item["Item"])

        user = user_dto.to_entity()

        expected_user = User(
            name="Bruno Soller",
            email="soller@soller.com",
            user_id=1,
            state=STATE.APPROVED
        )

        assert user.name == expected_user.name
        assert user.email == expected_user.email
        assert user.user_id == expected_user.user_id
        assert user.state == expected_user.state

    def test_from_entity_to_dynamo(self):
        repo = UserRepositoryMock()

        user_dto = UserDynamoDTO.from_entity(user=repo.users[0])

        user_dynamo = user_dto.to_dynamo()

        expected_dict = {
            "entity": "user",
            "name": repo.users[0].name,
            "email": repo.users[0].email,
            "user_id": repo.users[0].user_id,
            "state": repo.users[0].state.value
        }

        assert user_dynamo == expected_dict
