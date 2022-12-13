from src.modules.create_user.app.create_user_usecase import CreateUserUsecase
from src.modules.create_user.app.create_user_viewmodel import CreateUserViewmodel
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.helpers.http.http_models import HttpRequest, HttpResponse, NotFound, BadRequest, InternalServerError, \
    Created


class CreateUserController:

    def __init__(self, usecase: CreateUserUsecase):
        self.CreateUserUsecase = usecase

    def __call__(self, request: HttpRequest) -> HttpResponse:
        try:
            if request.query_params.get('name') is None:
                raise MissingParameters('name')
            if request.query_params.get('email') is None:
                raise MissingParameters('email')

            user = self.CreateUserUsecase(
                name=request.query_params.get('name'),
                email=request.query_params.get('email')
            )

            viewmodel = CreateUserViewmodel(user)

            return Created(viewmodel.to_dict())

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
