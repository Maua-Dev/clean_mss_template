from src.shared.domain.entities.item import Item


class GetItemViewmodel:
    def __init__(self, item: Item):
        self.item = item

    def to_dict(self):
        item_dict = self.item.model_dump(mode="json")
        item_dict["message"] = "the item was retrieved successfully"
        return item_dict
