from uuid import UUID

from src.shared.helpers.auth.authorizer_user import USER_FROM_AUTHORIZER_KEY
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from .auth_user_usecase import AuthUserUsecase
from .auth_user_viewmodel import AuthUserViewmodel
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import DuplicatedUser
from src.shared.helpers.external_interfaces.http_codes import (
    OK,
    Created,
    BadRequest,
    InternalServerError,
    Conflict,
)


class AuthUserController:

    def __init__(self, usecase: AuthUserUsecase):
        self.AuthUserUsecase = usecase

    def __call__(self, request: IRequest) -> IResponse:
        try:
            user_from_authorizer = request.data.get(USER_FROM_AUTHORIZER_KEY)

            if user_from_authorizer is None:
                raise MissingParameters(USER_FROM_AUTHORIZER_KEY)

            user_id = user_from_authorizer.get("sub")
            user_name = user_from_authorizer.get("name")
            user_email = user_from_authorizer.get("mail")

            if user_id is None:
                raise MissingParameters("sub")
            if user_name is None:
                raise MissingParameters("name")
            if user_email is None:
                raise MissingParameters("mail")

            if not isinstance(user_id, str):
                raise WrongTypeParameter(
                    fieldName="sub",
                    fieldTypeExpected="str",
                    fieldTypeReceived=type(user_id).__name__
                )
            if not isinstance(user_name, str):
                raise WrongTypeParameter(
                    fieldName="name",
                    fieldTypeExpected="str",
                    fieldTypeReceived=type(user_name).__name__
                )
            if not isinstance(user_email, str):
                raise WrongTypeParameter(
                    fieldName="mail",
                    fieldTypeExpected="str",
                    fieldTypeReceived=type(user_email).__name__
                )

            try:
                parsed_user_id = UUID(user_id)
            except ValueError:
                raise EntityError("user_id")

            user, case_number = self.AuthUserUsecase(
                user_id=parsed_user_id,
                user_name=user_name,
                user_email=user_email,
            )

            viewmodel = AuthUserViewmodel(user=user, case_number=case_number).to_dict()
            if case_number == 1:
                return Created(viewmodel)
            return OK(viewmodel)

        except MissingParameters as err:
            return BadRequest(body=err.message)
        except WrongTypeParameter as err:
            return BadRequest(body=err.message)
        except EntityError as err:
            return BadRequest(body=err.message)
        except DuplicatedUser as err:
            return Conflict(body=err.message)
        except Exception as err:
            return InternalServerError(body=err.args[0])
