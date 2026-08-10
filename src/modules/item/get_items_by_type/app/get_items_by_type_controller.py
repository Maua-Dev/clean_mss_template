from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from .get_items_by_type_usecase import GetItemsByTypeUsecase
from .get_items_by_type_viewmodel import GetItemsByTypeViewmodel
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.helpers.external_interfaces.http_codes import OK, NotFound, BadRequest, InternalServerError


class GetItemsByTypeController:

    def __init__(self, usecase: GetItemsByTypeUsecase):
        self.GetItemsByTypeUsecase = usecase

    def __call__(self, request: IRequest) -> IResponse:
        try:
            item_type = request.data.get("item_type")

            if item_type is None:
                raise MissingParameters("item_type")
            if not isinstance(item_type, str):
                raise WrongTypeParameter(
                    fieldName="item_type",
                    fieldTypeExpected="str",
                    fieldTypeReceived=type(item_type).__name__
                )

            items = self.GetItemsByTypeUsecase(item_type=item_type)
            return OK(GetItemsByTypeViewmodel(items).to_dict())

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
