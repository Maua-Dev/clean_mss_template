from src.shared.domain.entities.user import User
from src.shared.infra.external.dynamo.dynamo_keys import (
    EntityKind,
    build_gsi2_attributes,
    partition_key,
    sort_key,
    strip_keys,
)


class UserDynamoDTO:

    @staticmethod
    def from_entity_to_dynamo(user: User) -> dict:
        """
        Converts an User entity to a dictionary compatible with DynamoDB.

        Includes base keys (pk/sk).

        Args:
            user: The User entity to serialize.

        Returns:
            Dict as expected by DynamoDB put_item.
        """
        return {
            **user.model_dump(mode="json"),
            "pk": partition_key(kind=EntityKind.USER),
            "sk": sort_key(id=user.user_id, kind=EntityKind.USER),
            **build_gsi2_attributes(user.user_email, user.created_at),
        }

    @staticmethod
    def from_dynamo_to_entity(user_data: dict) -> User:
        """
        Converts a DynamoDB item dict into a User entity.

        Args:
            user_data: Dictionary from DynamoDB.

        Returns:
            User entity with storage keys removed.
        """
        return User.model_validate(obj=strip_keys(user_data))
