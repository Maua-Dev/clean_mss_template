from uuid import UUID

from src.shared.helpers.external_interfaces.external_interface import IResponse, IRequest
from .update_user_usecase import UpdateUserUsecase
from .update_user_viewmodel import UpdateUserViewmodel
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoUsersFound
from src.shared.helpers.external_interfaces.http_codes import OK, NotFound, BadRequest, InternalServerError


class UpdateUserController:

    def __init__(self, usecase: UpdateUserUsecase):
        self.UpdateUserUsecase = usecase

    def __call__(self, request: IRequest) -> IResponse:
        try:
            user_id = request.data.get("user_id")
            user_name = request.data.get("user_name")
            user_email = request.data.get("user_email")
            user_role = request.data.get("user_role")

            if user_id is None:
                raise MissingParameters("user_id")
            if user_name is None:
                raise MissingParameters("user_name")
            if user_email is None:
                raise MissingParameters("user_email")
            if user_role is None:
                raise MissingParameters("user_role")

            if not isinstance(user_id, str):
                raise WrongTypeParameter(
                    fieldName="user_id",
                    fieldTypeExpected="str",
                    fieldTypeReceived=type(user_id).__name__
                )
            if not isinstance(user_name, str):
                raise WrongTypeParameter(
                    fieldName="user_name",
                    fieldTypeExpected="str",
                    fieldTypeReceived=type(user_name).__name__
                )
            if not isinstance(user_email, str):
                raise WrongTypeParameter(
                    fieldName="user_email",
                    fieldTypeExpected="str",
                    fieldTypeReceived=type(user_email).__name__
                )
            if not isinstance(user_role, str):
                raise WrongTypeParameter(
                    fieldName="user_role",
                    fieldTypeExpected="str",
                    fieldTypeReceived=type(user_role).__name__
                )

            try:
                parsed_user_id = UUID(user_id)
            except ValueError:
                raise EntityError("user_id")

            user = self.UpdateUserUsecase(
                user_id=parsed_user_id,
                user_name=user_name,
                user_email=user_email,
                user_role=user_role,
            )

            return OK(UpdateUserViewmodel(user=user).to_dict())

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
