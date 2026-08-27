from typing import List

from src.shared.domain.entities.item import Item
from src.shared.domain.repositories.item_repository_interface import IItemRepository


class GetAllItemsUsecase:
    def __init__(self, item_repo: IItemRepository):
        self.item_repo = item_repo

    def __call__(self) -> List[Item]:
        return self.item_repo.get_all_item()
