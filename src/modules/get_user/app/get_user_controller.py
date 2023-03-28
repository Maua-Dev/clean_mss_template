from src.shared.infra.external.observability.observability_aws import ObservabilityAWS
from .get_user_usecase import GetUserUsecase
from .get_user_viewmodel import GetUserViewmodel
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import OK, NotFound, BadRequest, InternalServerError
from aws_lambda_powertools import Logger



class GetUserController:

    def __init__(self, usecase: GetUserUsecase, observability: ObservabilityAWS):
        self.GetUserUsecase = usecase
        self.observability = observability

    def __call__(self, request: IRequest) -> IResponse:
        try:
            self.observability.log_controller_in()
            if request.data.get('user_id') is None:
                raise MissingParameters('user_id')

            if type(request.data.get('user_id')) != str:
                raise WrongTypeParameter(
                    fieldName="user_id",
                    fieldTypeExpected="str",
                    fieldTypeReceived=request.data.get('user_id').__class__.__name__
                )

            if not request.data.get('user_id').isdecimal():
                raise EntityError("user_id")


            user = self.GetUserUsecase(
                user_id=int(request.data.get('user_id'))
            )

            viewmodel = GetUserViewmodel(user)
            
            response = OK(viewmodel.to_dict())
            self.observability.log_controller_out(input=user.user_id)
            return response

        except NoItemsFound as err:
            self.observability.log_exception(message=err.message)
            return NotFound(body=err.message)

        except MissingParameters as err:
            self.observability.log_exception(message=err.message)
            return BadRequest(body=err.message)

        except WrongTypeParameter as err:
            self.observability.log_exception(message=err.message)
            return BadRequest(body=err.message)

        except EntityError as err:
            self.observability.log_exception(message=err.message)
            return BadRequest(body=err.message)

        except Exception as err:
            self.observability.log_exception(message=err.args[0])
            return InternalServerError(body=err.args[0])
