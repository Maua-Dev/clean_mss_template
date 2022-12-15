
from .update_user_usecase import UpdateUserUsecase
from .update_user_viewmodel import UpdateUserViewmodel
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.helpers.external_interfaces.http_models import HttpRequest, HttpResponse
from src.shared.helpers.external_interfaces.http_codes import OK, NotFound, BadRequest, InternalServerError


class UpdateUserController:

    def __init__(self, usecase: UpdateUserUsecase):
        self.UpdateUserUsecase = usecase

    def __call__(self, request: HttpRequest) -> HttpResponse:
        try:
            if request.body.get('idUser') is None:
                raise MissingParameters('idUser')
            if request.body.get('new_name') is None:
                raise MissingParameters('new_name')

            if type(request.body.get('idUser')) != str:
                raise WrongTypeParameter(
                    fieldName="idUser",
                    fieldTypeExpected="str",
                    fieldTypeReceived=request.body.get('idUser').__class__.__name__
                )

            user = self.UpdateUserUsecase(idUser=int(request.body.get('idUser')), new_name=request.body.get('new_name'))

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
