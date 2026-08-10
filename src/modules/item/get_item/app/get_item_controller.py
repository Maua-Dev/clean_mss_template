from uuid import UUID

from .get_item_usecase import GetItemUsecase
from .get_item_viewmodel import GetItemViewmodel
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import OK, NotFound, BadRequest, InternalServerError


class GetItemController:

    def __init__(self, usecase: GetItemUsecase):
        self.GetItemUsecase = usecase

    def __call__(self, request: IRequest) -> IResponse:
        try:
            item_id = request.data.get("item_id")

            if item_id is None:
                raise MissingParameters("item_id")

            if not isinstance(item_id, str):
                raise WrongTypeParameter(
                    fieldName="item_id",
                    fieldTypeExpected="str",
                    fieldTypeReceived=type(item_id).__name__
                )

            try:
                parsed_item_id = UUID(item_id)
            except ValueError:
                raise EntityError("item_id")

            item = self.GetItemUsecase(item_id=parsed_item_id)

            viewmodel = GetItemViewmodel(item)

            return OK(viewmodel.to_dict())

        except NoItemsFound as err:
            return NotFound(body=err.message)

        except MissingParameters as err:
            return BadRequest(body=err.message)

        except WrongTypeParameter as err:
            return BadRequest(body=err.message)

        except EntityError as err:
            return BadRequest(body=err.message)

        except Exception as err:
            return InternalServerError(body=err.args[0])
