from uuid import UUID

from src.shared.domain.entities.item import Item
from src.shared.domain.repositories.item_repository_interface import IItemRepository


class DeleteItemUsecase:
    def __init__(self, repo: IItemRepository):
        self.repo = repo

    def __call__(self, item_id: UUID) -> Item:
        return self.repo.delete_item(item_id)
