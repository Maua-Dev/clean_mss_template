from typing import List

from src.shared.domain.entities.item import Item
from src.shared.domain.enums.item_type_enum import ItemTypeEnum
from src.shared.domain.repositories.item_repository_interface import IItemRepository
from src.shared.helpers.errors.domain_errors import EntityError


class GetItemsByTypeUsecase:
    def __init__(self, repo: IItemRepository):
        self.repo = repo

    def __call__(self, item_type: str) -> List[Item]:
        try:
            parsed_type = ItemTypeEnum(item_type)
        except ValueError as err:
            raise EntityError("item_type") from err

        return self.repo.get_items_by_type(parsed_type)
