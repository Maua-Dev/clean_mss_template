from src.modules.item.create_item.app.create_item_viewmodel import CreateItemViewmodel
from src.shared.infra.repositories.item_repository_mock import ItemRepositoryMock


class Test_CreateItemViewModel:
    def test_create_item_viewmodel(self):
        item_repo = ItemRepositoryMock()
        item = item_repo.items[0]
        result = CreateItemViewmodel(item=item).to_dict()

        assert result["item_id"] == str(item.item_id)
        assert result["item_name"] == item.item_name
        assert result["message"] == "the item was created successfully"
