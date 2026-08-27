from uuid import UUID

from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from .delete_user_usecase import DeleteUserUsecase
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoUsersFound
from src.shared.helpers.external_interfaces.http_codes import (
    NoContent,
    NotFound,
    BadRequest,
    InternalServerError,
)


class DeleteUserController:

    def __init__(self, usecase: DeleteUserUsecase):
        self.DeleteUserUsecase = usecase

    def __call__(self, request: IRequest) -> IResponse:
        try:
            user_id = request.data.get("user_id")

            if user_id is None:
                raise MissingParameters("user_id")
            if not isinstance(user_id, str):
                raise WrongTypeParameter(
                    fieldName="user_id",
                    fieldTypeExpected="str",
                    fieldTypeReceived=type(user_id).__name__
                )

            try:
                parsed_user_id = UUID(user_id)
            except ValueError:
                raise EntityError("user_id")

            self.DeleteUserUsecase(user_id=parsed_user_id)
            return NoContent()

        except NoUsersFound as err:
            return NotFound(body=err.message)
        except MissingParameters as err:
            return BadRequest(body=err.message)
        except WrongTypeParameter as err:
            return BadRequest(body=err.message)
        except EntityError as err:
            return BadRequest(body=err.message)
        except Exception as err:
            return InternalServerError(body=err.args[0])
