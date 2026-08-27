from src.modules.item.get_all_items.app.get_all_items_controller import GetAllItemsController
from src.modules.item.get_all_items.app.get_all_items_usecase import GetAllItemsUsecase
from src.shared.infra.repositories.item_repository_mock import ItemRepositoryMock


class Test_GetAllItemsController:
    def test_get_all_items_controller(self):
        item_repo = ItemRepositoryMock()
        usecase = GetAllItemsUsecase(item_repo)
        controller = GetAllItemsController(usecase)

        response = controller(None)

        assert response.status_code == 200
        assert len(response.body["all_items"]) == 3
        assert response.body["all_items"][0]["item_name"] == "Notebook"
        assert response.body["message"] == "all items have been retrieved"
