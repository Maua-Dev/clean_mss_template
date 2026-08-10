from src.modules.item.update_item.app.update_item_controller import UpdateItemController
from src.modules.item.update_item.app.update_item_usecase import UpdateItemUsecase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.item_repository_mock import ItemRepositoryMock


class Test_UpdateItemController:
    def test_update_item_controller(self):
        repo = ItemRepositoryMock()
        usecase = UpdateItemUsecase(repo=repo)
        controller = UpdateItemController(usecase=usecase)

        item = repo.items[0]
        request = HttpRequest(body={
            "item_id": str(item.item_id),
            "item_name": "Ultrabook",
            "item_description": "Updated description",
            "item_type": "type2",
            "item_image": "https://example.com/images/ultrabook.png"
        })

        response = controller(request=request)

        assert response.status_code == 200
        assert response.body["item_id"] == str(item.item_id)
        assert response.body["item_name"] == "Ultrabook"
        assert response.body["item_description"] == "Updated description"
        assert response.body["item_type"] == "type2"
        assert response.body["message"] == "the item was updated successfully"

    def test_update_item_controller_missing_item_id(self):
        repo = ItemRepositoryMock()
        usecase = UpdateItemUsecase(repo=repo)
        controller = UpdateItemController(usecase=usecase)

        request = HttpRequest(body={
            "item_name": "Ultrabook",
            "item_description": "Updated description",
            "item_type": "type2",
            "item_image": "https://example.com/images/ultrabook.png"
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "Field item_id is missing"

    def test_update_item_controller_missing_item_name(self):
        repo = ItemRepositoryMock()
        usecase = UpdateItemUsecase(repo=repo)
        controller = UpdateItemController(usecase=usecase)

        request = HttpRequest(body={
            "item_id": str(repo.items[0].item_id),
            "item_description": "Updated description",
            "item_type": "type2",
            "item_image": "https://example.com/images/ultrabook.png"
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "Field item_name is missing"

    def test_update_item_controller_wrong_type_item_id(self):
        repo = ItemRepositoryMock()
        usecase = UpdateItemUsecase(repo=repo)
        controller = UpdateItemController(usecase=usecase)

        request = HttpRequest(body={
            "item_id": 3,
            "item_name": "Ultrabook",
            "item_description": "Updated description",
            "item_type": "type2",
            "item_image": "https://example.com/images/ultrabook.png"
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == (
            "The field 'item_id' has the wrong type. Received: 'int'. Expected: 'str'."
        )

    def test_update_item_not_found(self):
        repo = ItemRepositoryMock()
        usecase = UpdateItemUsecase(repo=repo)
        controller = UpdateItemController(usecase=usecase)

        request = HttpRequest(body={
            "item_id": "99999999-9999-4999-8999-999999999999",
            "item_name": "Ultrabook",
            "item_description": "Updated description",
            "item_type": "type2",
            "item_image": "https://example.com/images/ultrabook.png"
        })

        response = controller(request=request)

        assert response.status_code == 404
        assert response.body == "No items found for item_id"
