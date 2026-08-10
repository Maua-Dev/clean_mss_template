from typing import List

from src.shared.domain.entities.item import Item
from src.shared.domain.repositories.item_repository_interface import IItemRepository


class GetAllItemsUsecase:
    def __init__(self, repo: IItemRepository):
        self.repo = repo

    def __call__(self) -> List[Item]:
        return self.repo.get_all_item()
