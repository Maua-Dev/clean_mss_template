from src.shared.helpers.errors.usecase_errors import NoItemsFound
from .delete_user_usecase import DeleteUserUsecase
from .delete_user_viewmodel import DeleteUserViewmodel
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.http.http_models import HttpRequest, HttpResponse, OK, NotFound, BadRequest, InternalServerError


class DeleteUserController:

    def __init__(self, usecase: DeleteUserUsecase):
        self.DeleteUserUsecase = usecase

    def __call__(self, request: HttpRequest) -> HttpResponse:
        try:
            if request.body.get('idUser') is None:
                raise MissingParameters('idUser')

            if type(request.body.get('idUser')) != str:
                raise EntityError("idUser")

            if not request.body.get('idUser').isdecimal():
                raise EntityError("idUser")

            user = self.DeleteUserUsecase(
                idUser=int(request.body.get('idUser'))
            )

            viewmodel = DeleteUserViewmodel(user=user)

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