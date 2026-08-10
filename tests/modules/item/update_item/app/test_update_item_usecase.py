from uuid import UUID

import pytest

from src.modules.item.update_item.app.update_item_usecase import UpdateItemUsecase
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.infra.repositories.item_repository_mock import ItemRepositoryMock


class Test_UpdateItemUsecase:
    def test_update_item(self):
        repo = ItemRepositoryMock()
        usecase = UpdateItemUsecase(repo)
        item = repo.items[0]

        updated = usecase(
            item_id=item.item_id,
            item_name="Ultrabook",
            item_description="Updated description",
            item_type="type2",
            item_image="https://example.com/images/ultrabook.png"
        )

        assert updated.item_id == item.item_id
        assert updated.item_name == "Ultrabook"
        assert updated.created_at == item.created_at
        assert repo.get_item(item.item_id).item_name == "Ultrabook"

    def test_update_item_not_found(self):
        repo = ItemRepositoryMock()
        usecase = UpdateItemUsecase(repo)

        with pytest.raises(NoItemsFound):
            usecase(
                item_id=UUID("99999999-9999-4999-8999-999999999999"),
                item_name="Ultrabook",
                item_description="Updated description",
                item_type="type2",
                item_image="https://example.com/images/ultrabook.png"
            )

    def test_update_item_invalid_name(self):
        repo = ItemRepositoryMock()
        usecase = UpdateItemUsecase(repo)

        with pytest.raises(EntityError):
            usecase(
                item_id=repo.items[0].item_id,
                item_name="   ",
                item_description="Updated description",
                item_type="type2",
                item_image="https://example.com/images/ultrabook.png"
            )
