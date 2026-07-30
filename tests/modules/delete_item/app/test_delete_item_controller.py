from uuid import UUID

from src.modules.delete_item.app.delete_item_controller import DeleteItemController
from src.modules.delete_item.app.delete_item_usecase import DeleteItemUsecase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.item_repository_mock import ItemRepositoryMock


class Test_DeleteItemController:
    def test_delete_item_controller(self):
        repo = ItemRepositoryMock()
        usecase = DeleteItemUsecase(repo=repo)
        controller = DeleteItemController(usecase=usecase)

        item_id = str(repo.items[0].item_id)
        request = HttpRequest(body={"item_id": item_id})

        response = controller(request=request)

        assert response.status_code == 200
        assert response.body["item_id"] == item_id
        assert response.body["item_name"] == "Notebook"
        assert response.body["message"] == "the item was deleted successfully"

    def test_delete_item_controller_invalid_uuid(self):
        repo = ItemRepositoryMock()
        usecase = DeleteItemUsecase(repo=repo)
        controller = DeleteItemController(usecase=usecase)

        request = HttpRequest(body={"item_id": "not-a-uuid"})

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "Field item_id is not valid"

    def test_delete_item_controller_missing_parameter(self):
        repo = ItemRepositoryMock()
        usecase = DeleteItemUsecase(repo=repo)
        controller = DeleteItemController(usecase=usecase)

        request = HttpRequest(body={"id": "1"})

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "Field item_id is missing"

    def test_delete_item_controller_wrong_type(self):
        repo = ItemRepositoryMock()
        usecase = DeleteItemUsecase(repo=repo)
        controller = DeleteItemController(usecase=usecase)

        request = HttpRequest(body={"item_id": 2})

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == (
            "The field 'item_id' has the wrong type. Received: 'int'. Expected: 'str'."
        )

    def test_delete_item_controller_no_items_found(self):
        repo = ItemRepositoryMock()
        usecase = DeleteItemUsecase(repo=repo)
        controller = DeleteItemController(usecase=usecase)

        request = HttpRequest(body={
            "item_id": "99999999-9999-4999-8999-999999999999"
        })

        response = controller(request=request)

        assert response.status_code == 404
        assert response.body == "No items found for item_id"
