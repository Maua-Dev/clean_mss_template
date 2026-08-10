from src.shared.domain.entities.item import Item
from src.shared.domain.repositories.item_repository_interface import IItemRepository


class CreateItemUsecase:
    def __init__(self, repo: IItemRepository):
        self.repo = repo

    def __call__(
        self,
        item_name: str,
        item_description: str,
        item_type: str,
        item_image: str
    ) -> Item:
        
        # validações são feitas durante a criação do objeto

        item = Item(
            item_name=item_name,
            item_description=item_description,
            item_type=item_type,
            item_image=item_image
        )

        return self.repo.create_item(item)
