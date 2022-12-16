from src.shared.infra.dto.user_dynamo_dto import UserDynamoDto
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_UserDynamoDto:
    def test_from_entity(self):

        repo = UserRepositoryMock()

        user_dto = UserDynamoDto.from_entity(user=repo.users[0])

        expected_selfie_dto = UserDynamoDto(
            name=repo.users[0].name,
            email=repo.users[0].email,
            idUser=repo.users[0].idUser,
            state=repo.users[0].state
        )

        assert user_dto == expected_selfie_dto

    def test_to_dynamo(self):

        repo = UserRepositoryMock()

        user_dto = UserDynamoDto(
            name=repo.users[0].name,
            email=repo.users[0].email,
            idUser=repo.users[0].idUser,
            state=repo.users[0].state
        )


        user_dynamo = user_dto.to_dynamo()

        expected_dict = {
            "entity": "user",
            "name": repo.users[0].name,
            "email": repo.users[0].email,
            "idUser": repo.users[0].idUser,
            "state": repo.users[0].state.value
        }

        assert user_dto.to_dynamo() == expected_dict

