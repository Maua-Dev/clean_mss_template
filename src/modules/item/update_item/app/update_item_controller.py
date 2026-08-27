from uuid import UUID

from src.shared.helpers.auth.authorizer_user import USER_FROM_AUTHORIZER_KEY
from src.shared.helpers.external_interfaces.external_interface import IResponse, IRequest
from .update_item_usecase import UpdateItemUsecase
from .update_item_viewmodel import UpdateItemViewmodel
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import ForbiddenAction, NoItemsFound
from src.shared.helpers.external_interfaces.http_codes import (
    OK,
    NotFound,
    BadRequest,
    InternalServerError,
    Forbidden,
)


class UpdateItemController:

    def __init__(self, usecase: UpdateItemUsecase):
        self.UpdateItemUsecase = usecase

    def __call__(self, request: IRequest) -> IResponse:
        try:
            user_from_authorizer = request.data.get(USER_FROM_AUTHORIZER_KEY)
            item_id = request.data.get("item_id")
            item_name = request.data.get("item_name")
            item_description = request.data.get("item_description")
            item_type = request.data.get("item_type")
            item_image = request.data.get("item_image")

            if item_id is None:
                raise MissingParameters("item_id")
            if item_name is None:
                raise MissingParameters("item_name")
            if item_description is None:
                raise MissingParameters("item_description")
            if item_type is None:
                raise MissingParameters("item_type")
            if item_image is None:
                raise MissingParameters("item_image")

            if not isinstance(item_id, str):
                raise WrongTypeParameter(
                    fieldName="item_id",
                    fieldTypeExpected="str",
                    fieldTypeReceived=type(item_id).__name__
                )
            if not isinstance(item_name, str):
                raise WrongTypeParameter(
                    fieldName="item_name",
                    fieldTypeExpected="str",
                    fieldTypeReceived=type(item_name).__name__
                )
            if not isinstance(item_description, str):
                raise WrongTypeParameter(
                    fieldName="item_description",
                    fieldTypeExpected="str",
                    fieldTypeReceived=type(item_description).__name__
                )
            if not isinstance(item_type, str):
                raise WrongTypeParameter(
                    fieldName="item_type",
                    fieldTypeExpected="str",
                    fieldTypeReceived=type(item_type).__name__
                )
            if not isinstance(item_image, str):
                raise WrongTypeParameter(
                    fieldName="item_image",
                    fieldTypeExpected="str",
                    fieldTypeReceived=type(item_image).__name__
                )

            try:
                parsed_item_id = UUID(item_id)
            except ValueError:
                raise EntityError("item_id")

            item = self.UpdateItemUsecase(
                item_id=parsed_item_id,
                item_name=item_name,
                item_description=item_description,
                item_type=item_type,
                item_image=item_image,
                user_from_authorizer=user_from_authorizer,
            )

            viewmodel = UpdateItemViewmodel(item=item)

            return OK(viewmodel.to_dict())

        except ForbiddenAction as err:
            return Forbidden(body=err.message)

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
