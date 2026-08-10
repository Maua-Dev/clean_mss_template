from aws_cdk import (
    aws_lambda as lambda_,
    aws_s3 as s3,
    aws_s3_notifications as s3n,
    Duration
)
from constructs import Construct
from aws_cdk.aws_apigateway import Resource, LambdaIntegration


class LambdaConstruct(Construct):
    
    stage: str
    stack_name: str
    functions_that_need_dynamo_db_access: list[lambda_.Function]
    functions_that_need_s3_access: list[lambda_.Function]
    functions_that_need_aurora_db_access: list[lambda_.Function]
    functions_that_need_other_permissions: list[lambda_.Function]
    lambda_layer: lambda_.LayerVersion

    def create_lambda_api_gateway_integration(
        self, 
        module_name: str,
        method: str, 
        api_resource: Resource,
        api_key_required: bool = False,
        environment_variables: dict = {"STAGE": "TEST"},
        public: bool = False,
        subfolder: str = "",
    ) -> lambda_.Function:
        
        code = lambda_.Code.from_asset(f"../src/modules/{subfolder}/{module_name}") if subfolder else lambda_.Code.from_asset(f"../src/modules/{module_name}")
        handler = f"app.{module_name}_presenter.lambda_handler"
        
        function = lambda_.Function(
            self, module_name.title(),
            code=code,
            handler=handler,
            function_name=f"{module_name}-{self.stack_name}-{self.stage}"[:63],
            runtime=lambda_.Runtime.PYTHON_3_13,
            layers=[self.lambda_layer],
            environment=environment_variables,
            timeout=Duration.seconds(60),
            memory_size=512
        )

        if public:
            api_resource.add_resource("public").add_resource(module_name.replace("_", "-")).add_method(
                method,
                integration=LambdaIntegration(function),
                api_key_required=api_key_required
            )
        else:
            api_resource.add_resource(module_name.replace("_", "-")).add_method(
                method,
                integration=LambdaIntegration(function),
                api_key_required=api_key_required
            )

        return function
    
    def create_lambda_s3_object_creation_deletion_trigger_integration(
        self,
        module_name: str,
        bucket: s3.Bucket,
        environment_variables: dict,
        deletion: bool = False,
        subfolder: str = "",
    ) -> lambda_.Function:
        
        code = lambda_.Code.from_asset(f"../src/modules/{subfolder}/{module_name}") if subfolder else lambda_.Code.from_asset(f"../src/modules/{module_name}")
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
            timeout=Duration.seconds(300), # tempo aumentando pois esse tipo de integracao envolve pdfs e bedrock (ate hoje)
            memory_size=1024
        )
        
        bucket.add_event_notification(
            s3.EventType.OBJECT_CREATED,
            s3n.LambdaDestination(function)
        )
        
        if deletion:
            bucket.add_event_notification(
                s3.EventType.OBJECT_REMOVED_DELETE,
                s3n.LambdaDestination(function)
            )
        
        return function
        

    def __init__(
        self, 
        scope: Construct,
        construct_id: str,
        stage: str,
        stack_name: str,
        api_gateway_resource: Resource,
        # bucket1: s3.Bucket,
        environment_variables: dict,
        **kargs
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
            # a pasta .build foi obtida do adjust layer directory, certifique-se de que a configuração da pasta layer gerada la esta igual
            code=lambda_.Code.from_asset("./build"),
            compatible_runtimes=[lambda_.Runtime.PYTHON_3_13]
        )
        
        self.create_user = self.create_lambda_api_gateway_integration(
            module_name="create_user", # nome da pasta
            method="POST",
            subfolder="user", # nome da subfolder ( se tiver )
            api_resource=api_gateway_resource,
            environment_variables=environment_variables,
        )
        self.functions_that_need_dynamo_db_access.append(self.create_user)
        
        # funções com exemplo em public e integração com ses para email
        # descomente esse código conforme for necessário, ficará aqui de exemplo
        # na dúvida, use public=False !!!!!!!!!
        
        # self.contact_us = self.create_lambda_api_gateway_integration(
        #     module_name="contact_us",
        #     method="POST",
        #     api_resource=api_gateway_resource,
        #     environment_variables=environment_variables,
        #     public=True
        # )
        
        # ses_send_policy = iam.PolicyStatement(
        #     effect=iam.Effect.ALLOW,
        #     actions=["ses:SendEmail"],
        #     resources=["*"],
        #     conditions={
        #         "StringEquals": {
        #             "ses:FromAddress": environment_variables.get("FROM_EMAIL")
        #         }
        #     }
        # )
        # self.contact_us.add_to_role_policy(ses_send_policy)
        
        # exemplo de função integrada com s3. tem uma relação com bedrock.

        # self.plans_extractor_function = self.create_lambda_s3_object_creation_deletion_trigger_integration(
        #     module_name="plans_extractor",
        #     bucket1 é requisitado e passado pelo init desse construct!
        #     bucket=bucket1,
        #     environment_variables=environment_variables
        # )
        
        # self.funtions_that_need_dynamo_db_access.append(self.plans_extractor_function)
        # self.functions_that_need_s3_bucket1_access.append(self.plans_extractor_function)
        # self.functions_that_need_other_permissions.append(self.plans_extractor_function) # permissao bedrock, por exemplo
        