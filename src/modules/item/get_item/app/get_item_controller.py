from uuid import UUID

from src.shared.domain.observability.observability_interface import IObservability
from .get_item_usecase import GetItemUsecase
from .get_item_viewmodel import GetItemViewmodel
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import OK, NotFound, BadRequest, InternalServerError


class GetItemController:

    def __init__(self, usecase: GetItemUsecase, observability: IObservability):
        self.GetItemUsecase = usecase
        self.observability = observability

    def __call__(self, request: IRequest) -> IResponse:
        try:
            self.observability.log_controller_in()

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

            response = OK(viewmodel.to_dict())
            self.observability.log_controller_out(input=str(item.item_id))
            return response

        except NoItemsFound as err:
            self.observability.log_exception(message=err.message)
            return NotFound(body=err.message)

        except MissingParameters as err:
            self.observability.log_exception(message=err.message)
            return BadRequest(body=err.message)

        except WrongTypeParameter as err:
            self.observability.log_exception(message=err.message)
            return BadRequest(body=err.message)

        except EntityError as err:
            self.observability.log_exception(message=err.message)
            return BadRequest(body=err.message)

        except Exception as err:
            self.observability.log_exception(message=err.args[0])
            return InternalServerError(body=err.args[0])
