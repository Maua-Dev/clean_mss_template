from src.modules.item.create_item.app.create_item_controller import CreateItemController
from src.modules.item.create_item.app.create_item_usecase import CreateItemUsecase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.item_repository_mock import ItemRepositoryMock


class Test_CreateItemController:
    def test_create_item_controller(self):
        repo = ItemRepositoryMock()
        usecase = CreateItemUsecase(repo=repo)
        controller = CreateItemController(usecase=usecase)

        request = HttpRequest(body={
            "item_name": "Monitor",
            "item_description": "27 inch 4K monitor",
            "item_type": "type1",
            "item_image": "https://example.com/images/monitor.png"
        })

        response = controller(request=request)

        assert response.status_code == 201
        assert response.body["item_name"] == "Monitor"
        assert response.body["item_description"] == "27 inch 4K monitor"
        assert response.body["item_type"] == "type1"
        assert response.body["message"] == "the item was created successfully"

    def test_create_item_controller_missing_item_name(self):
        repo = ItemRepositoryMock()
        usecase = CreateItemUsecase(repo=repo)
        controller = CreateItemController(usecase=usecase)

        request = HttpRequest(body={
            "item_description": "27 inch 4K monitor",
            "item_type": "type1",
            "item_image": "https://example.com/images/monitor.png"
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "Field item_name is missing"

    def test_create_item_controller_wrong_type(self):
        repo = ItemRepositoryMock()
        usecase = CreateItemUsecase(repo=repo)
        controller = CreateItemController(usecase=usecase)

        request = HttpRequest(body={
            "item_name": 123,
            "item_description": "27 inch 4K monitor",
            "item_type": "type1",
            "item_image": "https://example.com/images/monitor.png"
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == (
            "The field 'item_name' has the wrong type. Received: 'int'. Expected: 'str'."
        )

    def test_create_item_controller_invalid_image(self):
        repo = ItemRepositoryMock()
        usecase = CreateItemUsecase(repo=repo)
        controller = CreateItemController(usecase=usecase)

        request = HttpRequest(body={
            "item_name": "Monitor",
            "item_description": "27 inch 4K monitor",
            "item_type": "type1",
            "item_image": "not-a-url"
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "Field item_image is not valid"
