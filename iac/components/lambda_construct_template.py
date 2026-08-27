from typing import Optional

from aws_cdk import (
    aws_lambda as lambda_,
    aws_s3 as s3,
    aws_s3_notifications as s3n,
    aws_apigateway as apigw,
    Duration,
)
from constructs import Construct
from aws_cdk.aws_apigateway import Resource, LambdaIntegration, TokenAuthorizer


class LambdaConstruct(Construct):

    stage: str
    stack_name: str
    functions_that_need_dynamo_db_access: list[lambda_.Function]
    functions_that_need_s3_access: list[lambda_.Function]
    functions_that_need_aurora_db_access: list[lambda_.Function]
    functions_that_need_other_permissions: list[lambda_.Function]
    lambda_layer: lambda_.LayerVersion
    token_authorizer: TokenAuthorizer

    def create_lambda_function(
        self,
        module_name: str,
        environment_variables: dict = {"STAGE": "TEST"},
        subfolder: str = "",
    ) -> lambda_.Function:
        """Cria a Lambda do módulo (uma pasta = uma função)."""
        code = (
            lambda_.Code.from_asset(f"../src/modules/{subfolder}/{module_name}")
            if subfolder
            else lambda_.Code.from_asset(f"../src/modules/{module_name}")
        )
        return lambda_.Function(
            self,
            module_name.title().replace("_", ""),
            code=code,
            handler=f"app.{module_name}_presenter.lambda_handler",
            function_name=f"{module_name}-{self.stack_name}-{self.stage}"[:63],
            runtime=lambda_.Runtime.PYTHON_3_13,
            layers=[self.lambda_layer],
            environment=environment_variables,
            timeout=Duration.seconds(60),
            memory_size=512,
        )

    def add_method_to_resource(
        self,
        resource: Resource,
        method: str,
        function: lambda_.Function,
        authorizer: Optional[TokenAuthorizer] = None,
        api_key_required: bool = False,
    ) -> None:
        """Anexa um HTTP method a um resource já criado (REST path)."""
        method_options = {
            "integration": LambdaIntegration(function),
            "api_key_required": api_key_required,
        }
        if authorizer is not None:
            method_options["authorization_type"] = apigw.AuthorizationType.CUSTOM
            method_options["authorizer"] = authorizer
        else:
            method_options["authorization_type"] = apigw.AuthorizationType.NONE

        resource.add_method(method, **method_options)

    def create_lambda_s3_object_creation_deletion_trigger_integration(
        self,
        module_name: str,
        bucket: s3.Bucket,
        environment_variables: dict,
        deletion: bool = False,
        subfolder: str = "",
    ) -> lambda_.Function:

        code = (
            lambda_.Code.from_asset(f"../src/modules/{subfolder}/{module_name}")
            if subfolder
            else lambda_.Code.from_asset(f"../src/modules/{module_name}")
        )
        handler = f"app.{module_name}_presenter.lambda_handler"

        function: lambda_.Function = lambda_.Function(
            self,
            module_name.title(),
            code=code,
            handler=handler,
            function_name=f"{module_name}-{self.stack_name}-{self.stage}"[:63],
            runtime=lambda_.Runtime.PYTHON_3_13,
            layers=[self.lambda_layer],
            environment=environment_variables,
            timeout=Duration.seconds(300),
            memory_size=1024,
        )

        bucket.add_event_notification(
            s3.EventType.OBJECT_CREATED,
            s3n.LambdaDestination(function),
        )

        if deletion:
            bucket.add_event_notification(
                s3.EventType.OBJECT_REMOVED_DELETE,
                s3n.LambdaDestination(function),
            )

        return function

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        stage: str,
        stack_name: str,
        api_gateway_resource: Resource,
        environment_variables: dict,
        **kargs,
    ) -> None:

        super().__init__(scope, construct_id, **kargs)

        self.stage = stage
        self.stack_name = stack_name
        self.functions_that_need_dynamo_db_access = []
        self.functions_that_need_s3_access = []
        self.functions_that_need_aurora_db_access = []
        self.functions_that_need_other_permissions = []

        self.lambda_layer = lambda_.LayerVersion(
            self,
            id=f"{stack_name}_LambdaLayer_{stage}",
            layer_version_name=f"{stack_name}-LambdaLayer-{self.stage}",
            code=lambda_.Code.from_asset("./build"),
            compatible_runtimes=[lambda_.Runtime.PYTHON_3_13],
        )

        self.microsoft_authorizer_function = lambda_.Function(
            self,
            "MicrosoftAuthorizer",
            code=lambda_.Code.from_asset("../src/modules/microsoft_authorizer"),
            handler="app.microsoft_authorizer_presenter.lambda_handler",
            function_name=f"microsoft_authorizer-{self.stack_name}-{self.stage}"[:63],
            runtime=lambda_.Runtime.PYTHON_3_13,
            layers=[self.lambda_layer],
            environment=environment_variables,
            timeout=Duration.seconds(15),
            memory_size=512,
        )
        self.functions_that_need_dynamo_db_access.append(self.microsoft_authorizer_function)

        self.token_authorizer = apigw.TokenAuthorizer(
            self,
            "MicrosoftTokenAuthorizer",
            authorizer_name=f"microsoft-authorizer-{self.stack_name}-{self.stage}"[:63],
            handler=self.microsoft_authorizer_function,
            identity_source=apigw.IdentitySource.header("Authorization"),
            results_cache_ttl=Duration.seconds(0),
        )

        # --- REST resources (criados uma vez) ---
        auth_resource = api_gateway_resource.add_resource("auth")
        users_resource = api_gateway_resource.add_resource("users")
        user_id_resource = users_resource.add_resource("{user_id}")
        users_by_email_resource = users_resource.add_resource("by-email")
        items_resource = api_gateway_resource.add_resource("items")
        item_id_resource = items_resource.add_resource("{item_id}")
        items_by_type_resource = items_resource.add_resource("by-type")

        # --- User ---
        self.auth_user = self.create_lambda_function(
            module_name="auth_user",
            subfolder="user",
            environment_variables=environment_variables,
        )
        self.add_method_to_resource(
            auth_resource, "POST", self.auth_user, authorizer=self.token_authorizer
        )
        self.functions_that_need_dynamo_db_access.append(self.auth_user)

        self.create_user = self.create_lambda_function(
            module_name="create_user",
            subfolder="user",
            environment_variables=environment_variables,
        )
        self.add_method_to_resource(
            users_resource, "POST", self.create_user, authorizer=self.token_authorizer
        )
        self.functions_that_need_dynamo_db_access.append(self.create_user)

        self.get_all_users = self.create_lambda_function(
            module_name="get_all_users",
            subfolder="user",
            environment_variables=environment_variables,
        )
        self.add_method_to_resource(
            users_resource, "GET", self.get_all_users, authorizer=self.token_authorizer
        )
        self.functions_that_need_dynamo_db_access.append(self.get_all_users)

        self.get_user = self.create_lambda_function(
            module_name="get_user",
            subfolder="user",
            environment_variables=environment_variables,
        )
        self.add_method_to_resource(
            user_id_resource, "GET", self.get_user, authorizer=self.token_authorizer
        )
        self.functions_that_need_dynamo_db_access.append(self.get_user)

        self.update_user = self.create_lambda_function(
            module_name="update_user",
            subfolder="user",
            environment_variables=environment_variables,
        )
        self.add_method_to_resource(
            user_id_resource, "PUT", self.update_user, authorizer=self.token_authorizer
        )
        self.functions_that_need_dynamo_db_access.append(self.update_user)

        self.delete_user = self.create_lambda_function(
            module_name="delete_user",
            subfolder="user",
            environment_variables=environment_variables,
        )
        self.add_method_to_resource(
            user_id_resource, "DELETE", self.delete_user, authorizer=self.token_authorizer
        )
        self.functions_that_need_dynamo_db_access.append(self.delete_user)

        self.get_user_by_email = self.create_lambda_function(
            module_name="get_user_by_email",
            subfolder="user",
            environment_variables=environment_variables,
        )
        self.add_method_to_resource(
            users_by_email_resource,
            "GET",
            self.get_user_by_email,
            authorizer=self.token_authorizer,
        )
        self.functions_that_need_dynamo_db_access.append(self.get_user_by_email)

        # --- Item ---
        self.create_item = self.create_lambda_function(
            module_name="create_item",
            subfolder="item",
            environment_variables=environment_variables,
        )
        self.add_method_to_resource(
            items_resource, "POST", self.create_item, authorizer=self.token_authorizer
        )
        self.functions_that_need_dynamo_db_access.append(self.create_item)

        self.get_all_items = self.create_lambda_function(
            module_name="get_all_items",
            subfolder="item",
            environment_variables=environment_variables,
        )
        self.add_method_to_resource(
            items_resource, "GET", self.get_all_items, authorizer=self.token_authorizer
        )
        self.functions_that_need_dynamo_db_access.append(self.get_all_items)

        self.get_item = self.create_lambda_function(
            module_name="get_item",
            subfolder="item",
            environment_variables=environment_variables,
        )
        self.add_method_to_resource(
            item_id_resource, "GET", self.get_item, authorizer=self.token_authorizer
        )
        self.functions_that_need_dynamo_db_access.append(self.get_item)

        self.update_item = self.create_lambda_function(
            module_name="update_item",
            subfolder="item",
            environment_variables=environment_variables,
        )
        self.add_method_to_resource(
            item_id_resource, "PUT", self.update_item, authorizer=self.token_authorizer
        )
        self.functions_that_need_dynamo_db_access.append(self.update_item)

        self.delete_item = self.create_lambda_function(
            module_name="delete_item",
            subfolder="item",
            environment_variables=environment_variables,
        )
        self.add_method_to_resource(
            item_id_resource, "DELETE", self.delete_item, authorizer=self.token_authorizer
        )
        self.functions_that_need_dynamo_db_access.append(self.delete_item)

        self.get_items_by_type = self.create_lambda_function(
            module_name="get_items_by_type",
            subfolder="item",
            environment_variables=environment_variables,
        )
        self.add_method_to_resource(
            items_by_type_resource,
            "GET",
            self.get_items_by_type,
            authorizer=self.token_authorizer,
        )
        self.functions_that_need_dynamo_db_access.append(self.get_items_by_type)
