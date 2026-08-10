from uuid import UUID

from src.shared.domain.entities.item import Item
from src.shared.domain.repositories.item_repository_interface import IItemRepository


class UpdateItemUsecase:
    def __init__(self, repo: IItemRepository):
        self.repo = repo

    def __call__(
        self,
        item_id: UUID,
        item_name: str,
        item_description: str,
        item_type: str,
        item_image: str
    ) -> Item:
        existing = self.repo.get_item(item_id)

        updated_item = Item(
            item_id=existing.item_id,
            item_name=item_name,
            item_description=item_description,
            item_type=item_type,
            item_image=item_image,
            created_at=existing.created_at,
        )

        return self.repo.update_item(updated_item)
