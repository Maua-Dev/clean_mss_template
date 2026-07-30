from src.modules.get_item.app.get_item_viewmodel import GetItemViewmodel
from src.shared.infra.repositories.item_repository_mock import ItemRepositoryMock


class Test_GetItemViewmodel:
    def test_get_item_viewmodel(self):
        repo = ItemRepositoryMock()
        item = repo.items[0]
        result = GetItemViewmodel(item).to_dict()

        assert result["item_id"] == str(item.item_id)
        assert result["item_name"] == item.item_name
        assert result["message"] == "the item was retrieved successfully"
