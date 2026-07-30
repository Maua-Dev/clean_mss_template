from src.modules.get_item.app.get_item_controller import GetItemController
from src.modules.get_item.app.get_item_usecase import GetItemUsecase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.external.observability.observability_mock import ObservabilityMock
from src.shared.infra.repositories.item_repository_mock import ItemRepositoryMock

observability = ObservabilityMock(module_name="get_item")


class Test_GetItemController:
    def test_get_item_controller(self):
        repo = ItemRepositoryMock()
        usecase = GetItemUsecase(repo=repo, observability=observability)
        controller = GetItemController(usecase=usecase, observability=observability)

        item = repo.items[1]
        request = HttpRequest(query_params={"item_id": str(item.item_id)})

        response = controller(request=request)

        assert response.status_code == 200
        assert response.body["item_id"] == str(item.item_id)
        assert response.body["item_name"] == item.item_name
        assert response.body["item_description"] == item.item_description
        assert response.body["item_type"] == item.item_type.value
        assert response.body["message"] == "the item was retrieved successfully"

    def test_get_item_controller_missing_parameters(self):
        repo = ItemRepositoryMock()
        usecase = GetItemUsecase(repo=repo, observability=observability)
        controller = GetItemController(usecase=usecase, observability=observability)

        request = HttpRequest(query_params={})

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "Field item_id is missing"

    def test_get_item_controller_wrong_type_parameter(self):
        repo = ItemRepositoryMock()
        usecase = GetItemUsecase(repo=repo, observability=observability)
        controller = GetItemController(usecase=usecase, observability=observability)

        request = HttpRequest(query_params={"item_id": 999})

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == (
            "The field 'item_id' has the wrong type. Received: 'int'. Expected: 'str'."
        )

    def test_get_item_controller_entity_error(self):
        repo = ItemRepositoryMock()
        usecase = GetItemUsecase(repo=repo, observability=observability)
        controller = GetItemController(usecase=usecase, observability=observability)

        request = HttpRequest(query_params={"item_id": "abc"})

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "Field item_id is not valid"

    def test_get_item_controller_no_items_found(self):
        repo = ItemRepositoryMock()
        usecase = GetItemUsecase(repo=repo, observability=observability)
        controller = GetItemController(usecase=usecase, observability=observability)

        request = HttpRequest(query_params={
            "item_id": "99999999-9999-4999-8999-999999999999"
        })

        response = controller(request=request)

        assert response.status_code == 404
        assert response.body == "No items found for item_id"
