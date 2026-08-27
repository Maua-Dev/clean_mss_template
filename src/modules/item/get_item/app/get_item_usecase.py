from uuid import UUID

from src.shared.domain.entities.item import Item
from src.shared.domain.repositories.item_repository_interface import IItemRepository


class GetItemUsecase:
    def __init__(self, item_repo: IItemRepository):
        self.item_repo = item_repo

    def __call__(self, item_id: UUID) -> Item:
        return self.item_repo.get_item(item_id)
