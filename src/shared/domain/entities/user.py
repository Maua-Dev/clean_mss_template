import time
from typing import Annotated
from uuid import UUID, uuid4

from pydantic import BaseModel, EmailStr, Field, ValidationError

from src.shared.domain.enums.user_role_enum import UserRoleEnum
from src.shared.helpers.errors.domain_errors import EntityError


class User(BaseModel):

    def __init__(self, **data):
        try:
            super().__init__(**data)
        except ValidationError as err:
            raise EntityError(str(err.errors()[0]["loc"][0])) from err

    user_id: Annotated[
        UUID,
        Field(
            default_factory=uuid4,
            frozen=True,
            validate_default=True,
            title="User id",
            description="User id in uuid4 format"
        )
    ]

    user_name: Annotated[
        str,
        Field(
            max_length=30,
            min_length=2,
            title="User name",
            description="User name, visual usage in frontend"
        )
    ]

    user_email: Annotated[
        EmailStr,
        Field(
            title="User email",
            description="User email, used possibly as GSI"
        )
    ]

    user_role: Annotated[
        UserRoleEnum,
        Field(
            default=UserRoleEnum.USER,
            title="User role",
            description="User role, used to authorize actions"
        )
    ]

    created_at: Annotated[
        int,
        Field(
            default_factory=lambda: int(time.time()),
            validate_default=True,
            gt=0,
            frozen=True,
            title="Creation timestamp (seconds)",
            description="Created at timestamp in seconds, generated when object is created at runtime"
        )
    ]
