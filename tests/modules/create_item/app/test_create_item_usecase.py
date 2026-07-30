import pytest

from src.modules.create_item.app.create_item_usecase import CreateItemUsecase
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.infra.repositories.item_repository_mock import ItemRepositoryMock


class Test_CreateItemUsecase:
    def test_create_item(self):
        repo = ItemRepositoryMock()
        usecase = CreateItemUsecase(repo)

        item = usecase(
            item_name="Monitor",
            item_description="27 inch 4K monitor",
            item_type="type1",
            item_image="https://example.com/images/monitor.png"
        )

        assert repo.items[-1] == item
        assert item.item_name == "Monitor"

    def test_create_item_invalid_name(self):
        repo = ItemRepositoryMock()
        usecase = CreateItemUsecase(repo)

        with pytest.raises(EntityError):
            usecase(
                item_name="   ",
                item_description="27 inch 4K monitor",
                item_type="type1",
                item_image="https://example.com/images/monitor.png"
            )

    def test_create_item_invalid_type(self):
        repo = ItemRepositoryMock()
        usecase = CreateItemUsecase(repo)

        with pytest.raises(EntityError):
            usecase(
                item_name="Monitor",
                item_description="27 inch 4K monitor",
                item_type="invalid",
                item_image="https://example.com/images/monitor.png"
            )
