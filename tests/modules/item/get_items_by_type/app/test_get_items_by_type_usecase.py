import pytest

from src.modules.item.get_items_by_type.app.get_items_by_type_usecase import GetItemsByTypeUsecase
from src.shared.domain.enums.item_type_enum import ItemTypeEnum
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.infra.repositories.item_repository_mock import ItemRepositoryMock


class Test_GetItemsByTypeUsecase:
    def test_get_items_by_type(self):
        repo = ItemRepositoryMock()
        usecase = GetItemsByTypeUsecase(repo)

        items = usecase("type2")

        assert len(items) == 1
        assert items[0].item_type == ItemTypeEnum.TYPE2

    def test_get_items_by_type_invalid(self):
        repo = ItemRepositoryMock()
        usecase = GetItemsByTypeUsecase(repo)

        with pytest.raises(EntityError):
            usecase("nope")
