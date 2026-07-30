from typing import List

from src.shared.domain.entities.item import Item


class GetAllItemsViewmodel:
    def __init__(self, items_list: List[Item]):
        self.items_list = items_list

    def to_dict(self):
        return {
            "all_items": [item.model_dump(mode="json") for item in self.items_list],
            "message": "all items have been retrieved"
        }
