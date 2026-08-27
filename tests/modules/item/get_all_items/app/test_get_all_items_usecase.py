from src.modules.item.get_all_items.app.get_all_items_usecase import GetAllItemsUsecase
from src.shared.infra.repositories.item_repository_mock import ItemRepositoryMock


class Test_GetAllItemsUsecase:
    def test_get_all_items(self):
        item_repo = ItemRepositoryMock()
        usecase = GetAllItemsUsecase(item_repo)

        items = usecase()

        assert len(items) == 3
        assert items[0].item_name == "Notebook"
        assert items == item_repo.items
