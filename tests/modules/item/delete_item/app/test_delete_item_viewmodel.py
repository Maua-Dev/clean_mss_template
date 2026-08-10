from src.modules.item.delete_item.app.delete_item_viewmodel import DeleteItemViewmodel
from src.shared.infra.repositories.item_repository_mock import ItemRepositoryMock


class Test_DeleteItemViewmodel:
    def test_delete_item_viewmodel(self):
        repo = ItemRepositoryMock()
        item = repo.items[0]
        result = DeleteItemViewmodel(item=item).to_dict()

        assert result["item_id"] == str(item.item_id)
        assert result["item_name"] == item.item_name
        assert result["message"] == "the item was deleted successfully"
