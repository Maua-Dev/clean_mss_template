from uuid import UUID

from src.shared.domain.entities.item import Item
from src.shared.domain.repositories.item_repository_interface import IItemRepository
from src.shared.domain.observability.observability_interface import IObservability


class GetItemUsecase:
    def __init__(self, repo: IItemRepository, observability: IObservability):
        self.repo = repo
        self.observability = observability

    def __call__(self, item_id: UUID) -> Item:
        self.observability.log_usecase_in()
        item = self.repo.get_item(item_id)
        self.observability.log_usecase_out()
        return item
