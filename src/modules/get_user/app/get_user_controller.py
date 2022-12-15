from .get_user_usecase import GetUserUsecase
from .get_user_viewmodel import GetUserViewmodel
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import OK, NotFound, BadRequest, InternalServerError


class GetUserController:

    def __init__(self, usecase: GetUserUsecase):
        self.GetUserUsecase = usecase

    def __call__(self, request: IRequest) -> IResponse:
        try:
            if request.data.get('idUser') is None:
                raise MissingParameters('idUser')

            if type(request.data.get('idUser')) != str:
                raise WrongTypeParameter(
                    fieldName="idUser",
                    fieldTypeExpected="str",
                    fieldTypeReceived=request.data.get('idUser').__class__.__name__
                )

            if not request.data.get('idUser').isdecimal():
                raise EntityError("idUser")

            user = self.GetUserUsecase(
                idUser=int(request.data.get('idUser'))
            )

            viewmodel = GetUserViewmodel(user)

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
