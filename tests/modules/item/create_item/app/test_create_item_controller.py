from src.modules.item.create_item.app.create_item_controller import CreateItemController
from src.modules.item.create_item.app.create_item_usecase import CreateItemUsecase
from src.shared.helpers.auth.authorizer_user import USER_FROM_AUTHORIZER_KEY
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.item_repository_mock import ItemRepositoryMock
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock

# claims Microsoft (sub/mail/name). Role vem do DB via mail.
_ADMIN_CLAIMS = {
    "sub": "ms-admin",
    "mail": "alice@example.com",  # Admin no UserRepositoryMock
    "name": "Alice Admin",
}
_USER_CLAIMS = {
    "sub": "ms-user",
    "mail": "bob@example.com",  # User no UserRepositoryMock
    "name": "Bob User",
}


def _body(**fields):
    return {USER_FROM_AUTHORIZER_KEY: _ADMIN_CLAIMS, **fields}


class Test_CreateItemController:
    def test_create_item_controller(self):
        item_repo = ItemRepositoryMock()
        user_repo = UserRepositoryMock()
        usecase = CreateItemUsecase(item_repo, user_repo)
        controller = CreateItemController(usecase=usecase)

        request = HttpRequest(body=_body(
            item_name="Monitor",
            item_description="27 inch 4K monitor",
            item_type="type1",
            item_image="https://example.com/images/monitor.png"
        ))

        response = controller(request=request)

        assert response.status_code == 201
        assert response.body["item_name"] == "Monitor"
        assert response.body["item_description"] == "27 inch 4K monitor"
        assert response.body["item_type"] == "type1"
        assert response.body["message"] == "the item was created successfully"

    def test_create_item_controller_forbidden_without_authorizer_user(self):
        item_repo = ItemRepositoryMock()
        user_repo = UserRepositoryMock()
        usecase = CreateItemUsecase(item_repo, user_repo)
        controller = CreateItemController(usecase=usecase)

        request = HttpRequest(body={
            "item_name": "Monitor",
            "item_description": "27 inch 4K monitor",
            "item_type": "type1",
            "item_image": "https://example.com/images/monitor.png"
        })

        response = controller(request=request)

        assert response.status_code == 403
        assert response.body == "That action is forbidden for this user"

    def test_create_item_controller_forbidden_for_non_admin(self):
        item_repo = ItemRepositoryMock()
        user_repo = UserRepositoryMock()
        usecase = CreateItemUsecase(item_repo, user_repo)
        controller = CreateItemController(usecase=usecase)

        request = HttpRequest(body={
            USER_FROM_AUTHORIZER_KEY: _USER_CLAIMS,
            "item_name": "Monitor",
            "item_description": "27 inch 4K monitor",
            "item_type": "type1",
            "item_image": "https://example.com/images/monitor.png"
        })

        response = controller(request=request)

        assert response.status_code == 403
        assert response.body == "That action is forbidden for this user"

    def test_create_item_controller_missing_item_name(self):
        item_repo = ItemRepositoryMock()
        user_repo = UserRepositoryMock()
        usecase = CreateItemUsecase(item_repo, user_repo)
        controller = CreateItemController(usecase=usecase)

        request = HttpRequest(body=_body(
            item_description="27 inch 4K monitor",
            item_type="type1",
            item_image="https://example.com/images/monitor.png"
        ))

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "Field item_name is missing"

    def test_create_item_controller_wrong_type(self):
        item_repo = ItemRepositoryMock()
        user_repo = UserRepositoryMock()
        usecase = CreateItemUsecase(item_repo, user_repo)
        controller = CreateItemController(usecase=usecase)

        request = HttpRequest(body=_body(
            item_name=123,
            item_description="27 inch 4K monitor",
            item_type="type1",
            item_image="https://example.com/images/monitor.png"
        ))

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == (
            "The field 'item_name' has the wrong type. Received: 'int'. Expected: 'str'."
        )

    def test_create_item_controller_invalid_image(self):
        item_repo = ItemRepositoryMock()
        user_repo = UserRepositoryMock()
        usecase = CreateItemUsecase(item_repo, user_repo)
        controller = CreateItemController(usecase=usecase)

        request = HttpRequest(body=_body(
            item_name="Monitor",
            item_description="27 inch 4K monitor",
            item_type="type1",
            item_image="not-a-url"
        ))

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "Field item_image is not valid"
