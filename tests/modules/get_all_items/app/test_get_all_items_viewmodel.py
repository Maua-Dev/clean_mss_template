from src.modules.get_all_items.app.get_all_items_viewmodel import GetAllItemsViewmodel
from src.shared.infra.repositories.item_repository_mock import ItemRepositoryMock


class Test_GetAllItemsViewmodel:
    def test_get_all_items_viewmodel(self):
        repo = ItemRepositoryMock()
        result = GetAllItemsViewmodel(repo.items).to_dict()

        assert len(result["all_items"]) == 3
        assert result["all_items"][0]["item_id"] == str(repo.items[0].item_id)
        assert result["message"] == "all items have been retrieved"
