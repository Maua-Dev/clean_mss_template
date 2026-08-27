from src.modules.item.update_item.app.update_item_viewmodel import UpdateItemViewmodel
from src.shared.infra.repositories.item_repository_mock import ItemRepositoryMock


class Test_UpdateItemViewmodel:
    def test_update_item_viewmodel(self):
        item_repo = ItemRepositoryMock()
        item = item_repo.items[0]
        result = UpdateItemViewmodel(item=item).to_dict()

        assert result["item_id"] == str(item.item_id)
        assert result["item_name"] == item.item_name
        assert result["message"] == "the item was updated successfully"
