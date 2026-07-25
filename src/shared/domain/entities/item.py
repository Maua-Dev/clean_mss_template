

from typing import Annotated
from uuid import UUID, uuid4
from pydantic import AnyUrl, BaseModel, Field, field_validator
import time

from src.shared.domain.enums.item_type_enum import ItemTypeEnum
from src.shared.helpers.errors.domain_errors import EntityError


class Item(BaseModel):
    
    # detalhe: item_id e outros campos armazenam o tipo pythoniano, e nao o valor do uuid em string.
    # dito isso, no model dump (transição do objeto dynamo para entidade) precisamos inserir explicitamente
    # que queremos a saída em string, e nao pythoniana!
    # ......model_dump(mode="JSON")
    
    # o campo default factory faz um uuid automaticamente na criação da entidade, isso quer dizer que não precisamos
    # passar um id na hora de criar a entidade

    
    item_id: Annotated[
        UUID, 
        Field(
            default_factory=uuid4,
            frozen=True,
            validate_default=True,
            title="Item id",
            description="Item id in uuid4 format. Will be used as Dyano PK"
        )
    ]
    
    # @field_validator("item_id")
    # @classmethod
    # ...
    
    
    
    item_name: Annotated[
        str, 
        Field(
            max_length=30,
            title="Item name",
            description="Item name, visual usage in frontend"
        )
    ]
    
    @field_validator("item_name")
    @classmethod
    def name_must_not_be_blank(cls, value: str) -> str:
        if not value.strip():
            raise EntityError("item_name")
        return value.strip()
    
    
    
    item_description: str = Field(
        max_length=500,
        title="Item description",
        description="Item description, visual usage in frontend"
    )
    
    @field_validator("item_description")
    @classmethod
    def description_must_not_be_blank(cls, value: str) -> str:
        if not value.strip():
            raise EntityError("item_description")
        return value.strip()
    
    
    # como podemos escrever um capo não obrigatório:

    item_type: Annotated[
        ItemTypeEnum | None,
        Field(
            default=None,
            title="Item Type",
            description="Enum describing the type of item. Optional."
        )
    ]
    
    # @field_validator("item_type")
    # @classmethod
    # ...
    
        
    item_image: Annotated[
        AnyUrl,
        Field(
            title="Item image URL",
            description="URL of the item image stored in S3"
        )
    ]
    
    # @field_validator("item_image")
    # @classmethod
    # ...
    
    
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
    
    # @field_validator("created_at")
    # @classmethod
    # ...

