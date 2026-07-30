from src.shared.helpers.external_interfaces.external_interface import IResponse, IRequest
from .create_user_usecase import CreateUserUsecase
from .create_user_viewmodel import CreateUserViewmodel
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import DuplicatedUser, NoUsersFound
from src.shared.helpers.external_interfaces.http_codes import NotFound, BadRequest, InternalServerError, Created


class CreateUserController:

    def __init__(self, usecase: CreateUserUsecase):
        self.CreateUserUsecase = usecase

    def __call__(self, request: IRequest) -> IResponse:
        try:
            user_name = request.data.get("user_name")
            user_email = request.data.get("user_email")
            user_role = request.data.get("user_role")

            if user_name is None:
                raise MissingParameters("user_name")
            if user_email is None:
                raise MissingParameters("user_email")

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
            if user_role is not None and not isinstance(user_role, str):
                raise WrongTypeParameter(
                    fieldName="user_role",
                    fieldTypeExpected="str",
                    fieldTypeReceived=type(user_role).__name__
                )

            user = self.CreateUserUsecase(
                user_name=user_name,
                user_email=user_email,
                user_role=user_role,
            )

            viewmodel = CreateUserViewmodel(user)
            return Created(viewmodel.to_dict())

        except NoUsersFound as err:
            return NotFound(body=err.message)
        except DuplicatedUser as err:
            return BadRequest(body=err.message)
        except MissingParameters as err:
            return BadRequest(body=err.message)
        except WrongTypeParameter as err:
            return BadRequest(body=err.message)
        except EntityError as err:
            return BadRequest(body=err.message)
        except Exception as err:
            return InternalServerError(body=err.args[0])
