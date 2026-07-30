from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from .get_user_by_email_usecase import GetUserByEmailUsecase
from .get_user_by_email_viewmodel import GetUserByEmailViewmodel
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoUsersFound
from src.shared.helpers.external_interfaces.http_codes import OK, NotFound, BadRequest, InternalServerError


class GetUserByEmailController:

    def __init__(self, usecase: GetUserByEmailUsecase):
        self.GetUserByEmailUsecase = usecase

    def __call__(self, request: IRequest) -> IResponse:
        try:
            user_email = request.data.get("user_email")

            if user_email is None:
                raise MissingParameters("user_email")
            if not isinstance(user_email, str):
                raise WrongTypeParameter(
                    fieldName="user_email",
                    fieldTypeExpected="str",
                    fieldTypeReceived=type(user_email).__name__
                )

            user = self.GetUserByEmailUsecase(user_email=user_email)
            return OK(GetUserByEmailViewmodel(user).to_dict())

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
