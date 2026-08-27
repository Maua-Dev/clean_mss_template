from src.modules.item.update_item.app.update_item_controller import UpdateItemController
from src.modules.item.update_item.app.update_item_usecase import UpdateItemUsecase
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


def _request(item_id=None, claims=_ADMIN_CLAIMS, **fields):
    body = {USER_FROM_AUTHORIZER_KEY: claims, **fields}
    path_params = {"item_id": item_id} if item_id is not None else {}
    return HttpRequest(body=body, path_params=path_params)


class Test_UpdateItemController:
    def test_update_item_controller(self):
        item_repo = ItemRepositoryMock()
        user_repo = UserRepositoryMock()
        usecase = UpdateItemUsecase(item_repo, user_repo)
        controller = UpdateItemController(usecase=usecase)

        item = item_repo.items[0]
        request = _request(
            item_id=str(item.item_id),
            item_name="Ultrabook",
            item_description="Updated description",
            item_type="type2",
            item_image="https://example.com/images/ultrabook.png"
        )

        response = controller(request=request)

        assert response.status_code == 200
        assert response.body["item_id"] == str(item.item_id)
        assert response.body["item_name"] == "Ultrabook"
        assert response.body["item_description"] == "Updated description"
        assert response.body["item_type"] == "type2"
        assert response.body["message"] == "the item was updated successfully"

    def test_update_item_controller_forbidden_without_authorizer_user(self):
        item_repo = ItemRepositoryMock()
        user_repo = UserRepositoryMock()
        usecase = UpdateItemUsecase(item_repo, user_repo)
        controller = UpdateItemController(usecase=usecase)

        item = item_repo.items[0]
        request = HttpRequest(
            path_params={"item_id": str(item.item_id)},
            body={
                "item_name": "Ultrabook",
                "item_description": "Updated description",
                "item_type": "type2",
                "item_image": "https://example.com/images/ultrabook.png"
            },
        )

        response = controller(request=request)

        assert response.status_code == 403
        assert response.body == "That action is forbidden for this user"

    def test_update_item_controller_forbidden_for_non_admin(self):
        item_repo = ItemRepositoryMock()
        user_repo = UserRepositoryMock()
        usecase = UpdateItemUsecase(item_repo, user_repo)
        controller = UpdateItemController(usecase=usecase)

        item = item_repo.items[0]
        request = _request(
            item_id=str(item.item_id),
            claims=_USER_CLAIMS,
            item_name="Ultrabook",
            item_description="Updated description",
            item_type="type2",
            item_image="https://example.com/images/ultrabook.png"
        )

        response = controller(request=request)

        assert response.status_code == 403
        assert response.body == "That action is forbidden for this user"

    def test_update_item_controller_missing_item_id(self):
        item_repo = ItemRepositoryMock()
        user_repo = UserRepositoryMock()
        usecase = UpdateItemUsecase(item_repo, user_repo)
        controller = UpdateItemController(usecase=usecase)

        request = _request(
            item_name="Ultrabook",
            item_description="Updated description",
            item_type="type2",
            item_image="https://example.com/images/ultrabook.png"
        )

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "Field item_id is missing"

    def test_update_item_controller_missing_item_name(self):
        item_repo = ItemRepositoryMock()
        user_repo = UserRepositoryMock()
        usecase = UpdateItemUsecase(item_repo, user_repo)
        controller = UpdateItemController(usecase=usecase)

        request = _request(
            item_id=str(item_repo.items[0].item_id),
            item_description="Updated description",
            item_type="type2",
            item_image="https://example.com/images/ultrabook.png"
        )

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "Field item_name is missing"

    def test_update_item_controller_wrong_type_item_id(self):
        item_repo = ItemRepositoryMock()
        user_repo = UserRepositoryMock()
        usecase = UpdateItemUsecase(item_repo, user_repo)
        controller = UpdateItemController(usecase=usecase)

        request = _request(
            item_id=3,
            item_name="Ultrabook",
            item_description="Updated description",
            item_type="type2",
            item_image="https://example.com/images/ultrabook.png"
        )

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == (
            "The field 'item_id' has the wrong type. Received: 'int'. Expected: 'str'."
        )

    def test_update_item_not_found(self):
        item_repo = ItemRepositoryMock()
        user_repo = UserRepositoryMock()
        usecase = UpdateItemUsecase(item_repo, user_repo)
        controller = UpdateItemController(usecase=usecase)

        request = _request(
            item_id="99999999-9999-4999-8999-999999999999",
            item_name="Ultrabook",
            item_description="Updated description",
            item_type="type2",
            item_image="https://example.com/images/ultrabook.png"
        )

        response = controller(request=request)

        assert response.status_code == 404
        assert response.body == "No items found for item_id"
