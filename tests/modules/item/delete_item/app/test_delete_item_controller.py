from src.modules.item.delete_item.app.delete_item_controller import DeleteItemController
from src.modules.item.delete_item.app.delete_item_usecase import DeleteItemUsecase
from src.shared.helpers.auth.authorizer_user import USER_FROM_AUTHORIZER_KEY
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.item_repository_mock import ItemRepositoryMock
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock

_ADMIN_CLAIMS = {
    "sub": "ms-admin",
    "mail": "alice@example.com",
    "name": "Alice Admin",
}
_USER_CLAIMS = {
    "sub": "ms-user",
    "mail": "bob@example.com",
    "name": "Bob User",
}


class Test_DeleteItemController:
    def test_delete_item_controller(self):
        item_repo = ItemRepositoryMock()
        user_repo = UserRepositoryMock()
        usecase = DeleteItemUsecase(item_repo, user_repo)
        controller = DeleteItemController(usecase=usecase)

        item_id = str(item_repo.items[0].item_id)
        request = HttpRequest(body={
            USER_FROM_AUTHORIZER_KEY: _ADMIN_CLAIMS,
            "item_id": item_id,
        })

        response = controller(request=request)

        assert response.status_code == 200
        assert response.body["item_id"] == item_id
        assert response.body["item_name"] == "Notebook"
        assert response.body["message"] == "the item was deleted successfully"

    def test_delete_item_controller_forbidden_without_authorizer_user(self):
        item_repo = ItemRepositoryMock()
        user_repo = UserRepositoryMock()
        usecase = DeleteItemUsecase(item_repo, user_repo)
        controller = DeleteItemController(usecase=usecase)

        request = HttpRequest(body={"item_id": str(item_repo.items[0].item_id)})

        response = controller(request=request)

        assert response.status_code == 403
        assert response.body == "That action is forbidden for this user"

    def test_delete_item_controller_forbidden_for_non_admin(self):
        item_repo = ItemRepositoryMock()
        user_repo = UserRepositoryMock()
        usecase = DeleteItemUsecase(item_repo, user_repo)
        controller = DeleteItemController(usecase=usecase)

        request = HttpRequest(body={
            USER_FROM_AUTHORIZER_KEY: _USER_CLAIMS,
            "item_id": str(item_repo.items[0].item_id),
        })

        response = controller(request=request)

        assert response.status_code == 403
        assert response.body == "That action is forbidden for this user"

    def test_delete_item_controller_invalid_uuid(self):
        item_repo = ItemRepositoryMock()
        user_repo = UserRepositoryMock()
        usecase = DeleteItemUsecase(item_repo, user_repo)
        controller = DeleteItemController(usecase=usecase)

        request = HttpRequest(body={
            USER_FROM_AUTHORIZER_KEY: _ADMIN_CLAIMS,
            "item_id": "not-a-uuid",
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "Field item_id is not valid"

    def test_delete_item_controller_missing_parameter(self):
        item_repo = ItemRepositoryMock()
        user_repo = UserRepositoryMock()
        usecase = DeleteItemUsecase(item_repo, user_repo)
        controller = DeleteItemController(usecase=usecase)

        request = HttpRequest(body={
            USER_FROM_AUTHORIZER_KEY: _ADMIN_CLAIMS,
            "id": "1",
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "Field item_id is missing"

    def test_delete_item_controller_wrong_type(self):
        item_repo = ItemRepositoryMock()
        user_repo = UserRepositoryMock()
        usecase = DeleteItemUsecase(item_repo, user_repo)
        controller = DeleteItemController(usecase=usecase)

        request = HttpRequest(body={
            USER_FROM_AUTHORIZER_KEY: _ADMIN_CLAIMS,
            "item_id": 2,
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == (
            "The field 'item_id' has the wrong type. Received: 'int'. Expected: 'str'."
        )

    def test_delete_item_controller_no_items_found(self):
        item_repo = ItemRepositoryMock()
        user_repo = UserRepositoryMock()
        usecase = DeleteItemUsecase(item_repo, user_repo)
        controller = DeleteItemController(usecase=usecase)

        request = HttpRequest(body={
            USER_FROM_AUTHORIZER_KEY: _ADMIN_CLAIMS,
            "item_id": "99999999-9999-4999-8999-999999999999",
        })

        response = controller(request=request)

        assert response.status_code == 404
        assert response.body == "No items found for item_id"
