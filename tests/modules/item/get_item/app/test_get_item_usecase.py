from uuid import UUID

import pytest

from src.modules.item.get_item.app.get_item_usecase import GetItemUsecase
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.infra.external.observability.observability_mock import ObservabilityMock
from src.shared.infra.repositories.item_repository_mock import ItemRepositoryMock

observability = ObservabilityMock(module_name="get_item")


class Test_GetItemUsecase:
    def test_get_item(self):
        repo = ItemRepositoryMock()
        usecase = GetItemUsecase(repo, observability=observability)
        item = repo.items[0]

        result = usecase(item_id=item.item_id)

        assert result == item

    def test_get_item_not_found(self):
        repo = ItemRepositoryMock()
        usecase = GetItemUsecase(repo, observability=observability)

        with pytest.raises(NoItemsFound):
            usecase(item_id=UUID("99999999-9999-4999-8999-999999999999"))
