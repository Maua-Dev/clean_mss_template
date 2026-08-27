from src.modules.item.get_items_by_type.app.get_items_by_type_viewmodel import GetItemsByTypeViewmodel
from src.shared.infra.repositories.item_repository_mock import ItemRepositoryMock


class Test_GetItemsByTypeViewmodel:
    def test_get_items_by_type_viewmodel(self):
        item_repo = ItemRepositoryMock()
        items = item_repo.get_items_by_type(item_repo.items[0].item_type)
        result = GetItemsByTypeViewmodel(items).to_dict()
        assert len(result["items"]) == 1
