from src.modules.item.get_items_by_type.app.get_items_by_type_controller import GetItemsByTypeController
from src.modules.item.get_items_by_type.app.get_items_by_type_usecase import GetItemsByTypeUsecase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.item_repository_mock import ItemRepositoryMock


class Test_GetItemsByTypeController:
    def test_get_items_by_type_controller(self):
        repo = ItemRepositoryMock()
        controller = GetItemsByTypeController(GetItemsByTypeUsecase(repo))

        response = controller(HttpRequest(query_params={"item_type": "type1"}))

        assert response.status_code == 200
        assert len(response.body["items"]) == 1
        assert response.body["items"][0]["item_name"] == "Notebook"
        assert response.body["message"] == "items by type have been retrieved"

    def test_get_items_by_type_invalid(self):
        repo = ItemRepositoryMock()
        controller = GetItemsByTypeController(GetItemsByTypeUsecase(repo))

        response = controller(HttpRequest(query_params={"item_type": "invalid"}))

        assert response.status_code == 400
        assert response.body == "Field item_type is not valid"

    def test_get_items_by_type_missing(self):
        repo = ItemRepositoryMock()
        controller = GetItemsByTypeController(GetItemsByTypeUsecase(repo))

        response = controller(HttpRequest(query_params={}))

        assert response.status_code == 400
