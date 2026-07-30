from src.shared.domain.enums.user_role_enum import UserRoleEnum
from src.shared.infra.dto.user_dynamo_dto import UserDynamoDTO
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_UserDynamoDTO:
    def test_from_entity_to_dynamo(self):
        user = UserRepositoryMock().users[0]
        data = UserDynamoDTO.from_entity_to_dynamo(user)

        assert data["pk"] == "USER"
        assert data["sk"] == f"USER#{user.user_id}"
        assert data["gsi2pk"] == "EMAIL#alice@example.com"
        assert data["gsi2sk"] == f"{user.created_at:013d}"
        assert data["user_role"] == "Admin"

    def test_from_dynamo_to_entity_roundtrip(self):
        user = UserRepositoryMock().users[1]
        dynamo = UserDynamoDTO.from_entity_to_dynamo(user)
        restored = UserDynamoDTO.from_dynamo_to_entity(dynamo)

        assert restored.user_id == user.user_id
        assert restored.user_email == user.user_email
        assert restored.user_role == UserRoleEnum.USER
