import os

import pytest

from src.shared.helpers.errors.usecase_errors import DuplicatedItem, NoItemsFound
from src.shared.infra.repositories.item_repository_dynamo import ItemRepositoryDynamo
from src.shared.infra.repositories.item_repository_mock import ItemRepositoryMock


class Test_ItemRepositoryDynamo:

    @pytest.mark.skip(reason="Needs dynamoDB")
    def test_create_item(self):
        os.environ["STAGE"] = "TEST"

        item_repository = ItemRepositoryDynamo()
        item_repository_mock = ItemRepositoryMock()
        resp = item_repository.create_item(item_repository_mock.items[0])

        assert item_repository_mock.items[0].item_name == resp.item_name
        assert item_repository_mock.items[0].item_id == resp.item_id

    @pytest.mark.skip(reason="Needs dynamoDB")
    def test_get_item(self):
        os.environ["STAGE"] = "TEST"

        item_repository = ItemRepositoryDynamo()
        item_repository_mock = ItemRepositoryMock()
        item = item_repository_mock.items[0]
        
        resp = item_repository.get_item(item.item_id)

        assert resp.item_id == item.item_id
        assert resp.item_name == item.item_name

    @pytest.mark.skip(reason="Needs dynamoDB")
    def test_get_all_item(self):
        os.environ["STAGE"] = "TEST"

        item_repository = ItemRepositoryDynamo()
        item_repository_mock = ItemRepositoryMock()

        resp = item_repository.get_all_item()

        assert len(resp) >= 3

    @pytest.mark.skip(reason="Needs dynamoDB")
    def test_get_items_by_type(self):
        os.environ["STAGE"] = "TEST"

        item_repository = ItemRepositoryDynamo()
        item_repository_mock = ItemRepositoryMock()
        item = item_repository_mock.items[0]

        resp = item_repository.get_items_by_type(item.item_type)

        assert len(resp) >= 1
        assert all(i.item_type == item.item_type for i in resp)

    @pytest.mark.skip(reason="Needs dynamoDB")
    def test_update_item(self):
        os.environ["STAGE"] = "TEST"

        item_repository = ItemRepositoryDynamo()
        item_repository_mock = ItemRepositoryMock()
        item = item_repository_mock.items[0]

        updated = item.model_copy(update={"item_name": "Ultrabook"})
        resp = item_repository.update_item(updated)

        assert resp.item_name == "Ultrabook"
        assert item_repository.get_item(item.item_id).item_name == "Ultrabook"

    @pytest.mark.skip(reason="Needs dynamoDB")
    def test_delete_item(self):
        os.environ["STAGE"] = "TEST"

        item_repository = ItemRepositoryDynamo()
        item_repository_mock = ItemRepositoryMock()
        item = item_repository_mock.items[1]

        resp = item_repository.delete_item(item.item_id)

        assert resp.item_id == item.item_id
        with pytest.raises(NoItemsFound):
            item_repository.get_item(item.item_id)

    @pytest.mark.skip(reason="Needs dynamoDB")
    def test_get_item_counter(self):
        os.environ["STAGE"] = "TEST"

        item_repository = ItemRepositoryDynamo()
        item_repository_mock = ItemRepositoryMock()

        assert item_repository.get_item_counter() >= 3
