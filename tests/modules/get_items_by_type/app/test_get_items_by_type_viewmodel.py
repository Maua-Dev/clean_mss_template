from src.modules.get_items_by_type.app.get_items_by_type_viewmodel import GetItemsByTypeViewmodel
from src.shared.infra.repositories.item_repository_mock import ItemRepositoryMock


class Test_GetItemsByTypeViewmodel:
    def test_get_items_by_type_viewmodel(self):
        repo = ItemRepositoryMock()
        items = repo.get_items_by_type(repo.items[0].item_type)
        result = GetItemsByTypeViewmodel(items).to_dict()
        assert len(result["items"]) == 1
