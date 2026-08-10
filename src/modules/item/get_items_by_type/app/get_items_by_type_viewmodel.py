from typing import List

from src.shared.domain.entities.item import Item


class GetItemsByTypeViewmodel:
    def __init__(self, items_list: List[Item]):
        self.items_list = items_list

    def to_dict(self):
        return {
            "items": [item.model_dump(mode="json") for item in self.items_list],
            "message": "items by type have been retrieved"
        }
