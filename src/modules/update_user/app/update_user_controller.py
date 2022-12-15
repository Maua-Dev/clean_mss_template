from src.shared.helpers.external_interfaces.external_interface import IResponse, IRequest
from .update_user_usecase import UpdateUserUsecase
from .update_user_viewmodel import UpdateUserViewmodel
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.helpers.external_interfaces.http_codes import OK, NotFound, BadRequest, InternalServerError


class UpdateUserController:

    def __init__(self, usecase: UpdateUserUsecase):
        self.UpdateUserUsecase = usecase

    def __call__(self, request: IRequest) -> IResponse:
        try:
            if request.data.get('idUser') is None:
                raise MissingParameters('idUser')
            if request.data.get('new_name') is None:
                raise MissingParameters('new_name')

            if type(request.data.get('idUser')) != str:
                raise WrongTypeParameter(
                    fieldName="idUser",
                    fieldTypeExpected="str",
                    fieldTypeReceived=request.data.get('idUser').__class__.__name__
                )

            user = self.UpdateUserUsecase(idUser=int(request.data.get('idUser')), new_name=request.data.get('new_name'))

            viewmodel = UpdateUserViewmodel(user=user)

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
