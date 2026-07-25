"""Convenções de chaves Dynamo (tabela base + GSI1).

Tabela base:
  pk = ITEM
  sk = ITEM#<uuid>

GSI1 (ItemTypeIndex) — access pattern secundário "items por tipo":
  gsi1pk = TYPE#<type>
  gsi1sk = created_at zero-padded
  sparse: omitir gsi1* quando item_type is None

Uso no repository Dynamo (exemplo)::

    from boto3.dynamodb.conditions import Key
    from src.shared.infra.external.dynamo.dynamo_keys import (
        GSI1_NAME, GSI1_PK_ATTR, gsi1_partition_key,
    )

    resp = self.dynamo.query(
        KeyConditionExpression=Key(GSI1_PK_ATTR).eq(gsi1_partition_key(item_type)),
        IndexName=GSI1_NAME,
    )
"""

from enum import Enum
from typing import Any, Optional
from uuid import UUID

from src.shared.domain.enums.item_type_enum import ItemTypeEnum

# Nomes dos atributos da tabela base (alinhados ao CDK: pk/sk)
PK_ATTR = "pk"
SK_ATTR = "sk"

# GSI1 — access pattern: listar items por tipo, ordenados por created_at
# Alinhado a iac/components/dynamo_construct_template.py (ItemTypeIndex)
GSI1_NAME = "ItemTypeIndex"
GSI1_PK_ATTR = "gsi1pk"
GSI1_SK_ATTR = "gsi1sk"

STORAGE_KEY_ATTRS = (PK_ATTR, SK_ATTR, GSI1_PK_ATTR, GSI1_SK_ATTR)


class EntityKind(str, Enum):
    ITEM = "ITEM"


def partition_key(kind: EntityKind = EntityKind.ITEM) -> str:
    """PK da tabela base — coleção (se repete para todos os items)."""
    return kind.value


def sort_key(item_id: UUID, kind: EntityKind = EntityKind.ITEM) -> str:
    """SK da tabela base — identidade única dentro da coleção."""
    return f"{kind.value}#{item_id}"


def gsi1_partition_key(item_type: ItemTypeEnum) -> str:
    """
    PK do GSI1 — agrupa por tipo.

    Ex.: TYPE#type1
    """
    return f"TYPE#{item_type.value}"


def gsi1_sort_key(created_at: int) -> str:
    """
    SK do GSI1 — ordenação por created_at (string zero-padded).

    Ex.: 0001700000000
    """
    return f"{created_at:013d}"


def build_gsi1_attributes(
    item_type: Optional[ItemTypeEnum],
    created_at: int,
) -> dict[str, str]:
    """
    Índice sparse: só escreve gsi1pk/gsi1sk quando item_type está definido.
    Items sem tipo não entram no ItemTypeIndex.
    """
    if item_type is None:
        return {}

    return {
        GSI1_PK_ATTR: gsi1_partition_key(item_type),
        GSI1_SK_ATTR: gsi1_sort_key(created_at),
    }


def strip_keys(item: dict[str, Any]) -> dict[str, Any]:
    """Remove atributos de storage (pk/sk/gsi) antes do model_validate."""
    return {k: v for k, v in item.items() if k not in STORAGE_KEY_ATTRS}
