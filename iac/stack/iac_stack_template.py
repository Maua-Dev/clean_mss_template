import os
from aws_cdk import (
    Stack,
    aws_iam as iam
)
from constructs import Construct

from components.apigw_construct_template import ApigwConstruct
from components.dynamo_construct_template import DynamoConstruct
from components.lambda_construct_template import LambdaConstruct
from components.s3_construct_template import S3Construct
from components.ssm_construct_template import SsmConstruct
from components.sm_construct_template import SmConstruct
from components.aurora_construct_template import AuroraConstruct

class IacStack(Stack):
    
    def __init__(
        self, 
        scope: Construct,
        stack_id: str,
        stack_name: str,
        stage: str,
        **kwargs
    ) -> None:
        
        super().__init__(scope, stack_id, **kwargs)

        self.github_ref_name = os.environ.get("GITHUB_REF_NAME", "")
        self.aws_region = os.environ.get("AWS_REGION")
        self.s3_assets_cdn = os.environ.get("S3_ASSETS_CDN")

        self.apigw_construct = ApigwConstruct(
            self, 
            construct_id=f"Apigw",
            stack_name=stack_name,
            stage=stage
        )
        
        # self.s3_construct = S3Construct(
        #     self, 
        #     construct_id=f"S3", 
        #     stage=stage
        # )

        self.dynamo_construct = DynamoConstruct(
            self,
            construct_id=f"Dynamo",
            stack_name=stack_name,
            stage=stage,
        )
        
        # self.sm_construct = SmConstruct(
        #     self, 
        #     construct_id=f"SecretsManager",
        #     stack_name=stack_name,
        #     stage=stage,
        # )
        
        # self.aurora_construct = AuroraConstruct(
        #     self, 
        #     construct_id="Aurora",
        #     stack_name=stack_name,
        #     stage=stage
        # )

        # alinhado com Environments.load_envs() (stages DEV/HOMOLOG/PROD)
        ENVIRONMENT_VARIABLES = {
            "STAGE": stage.upper(),
            "REGION": self.region,
            "DYNAMO_TABLE_NAME": self.dynamo_construct.template_table1.table_name,
            "DYNAMO_PARTITION_KEY": "pk",
            "DYNAMO_SORT_KEY": "sk",
            "MSS_NAME": stack_name,
            "GRAPH_MICROSOFT_ENDPOINT": os.environ.get(
                "GRAPH_MICROSOFT_ENDPOINT",
                "https://graph.microsoft.com/v1.0/me", #não há problema em exibir esse endpoint
            ),
            # "EVENT_SECRET_ARN": self.sm_construct.event_secret.secret_arn
            # variaveis acessives às funções lambda
            # coisas como bucket name, table name etc...
        }

        self.lambda_construct = LambdaConstruct(
            self, 
            construct_id=f"Lambda",
            api_gateway_resource=self.apigw_construct.api_gateway_resource,
            stage=stage,
            stack_name=stack_name,
            # bucket1=self.s3_construct.bucket1,
            environment_variables=ENVIRONMENT_VARIABLES
        )
                
        # instância SSM manager para passar automaticamente variáveis a um hub de "segredos"
        # da prórpia conta, evitando ter que manualmente passa-las para o github secrets
        
        # isso evita problemas de discrepância nos endpoints
        
        # atenção aqui, isso DEVE suprir o que estamos precisando / pegando de variáveis de 
        # ambiente no CD do front vinda do BACK ( nada de route 53 aqui )
        
        # esse construct exige um apigw
        # path SSM: /{stack_name}/{stage}/api/url  (mesmo STACK_NAME do CD)
        
        self.ssm_construct = SsmConstruct(
            self,
            stage=stage,
            construct_id=f"{stack_name}SystemsManager",
            stack_name=stack_name,
            api=self.apigw_construct.rest_api,
            api_gateway_resource=self.apigw_construct.api_gateway_resource,
            buckets=None, # o que deve ser salvo são os CDNs, visto que os buckets devem bloquear acesso pela URL publica
            # extra_params={
            #     "cdn/bucket1": self.s3_construct.cloudfront_distribution_bucket1.distribution_domain_name
            # }
        )
        
        for function in self.lambda_construct.functions_that_need_dynamo_db_access:
            self.dynamo_construct.template_table1.grant_read_write_data(function)
            
        # for function in self.lambda_construct.functions_that_need_aurora_db_access:
        #     self.aurora_construct.cluster.grant_data_api_access(function)
        #     self.aurora_construct.secret.grant_read(function)
            
        # for function in self.lambda_construct.functions_that_need_s3_access:
        #     self.s3_construct.bucket1.grant_read_write(function)
            
        # for function in self.lambda_construct.functions_that_need_other_permissions:
    
        #     bedrock_policy = iam.PolicyStatement(
        #         effect=iam.Effect.ALLOW,
        #         actions=[
        #             "bedrock:InvokeModel",
        #             "aws-marketplace:ViewSubscriptions",
        #             "aws-marketplace:Subscribe"
        #         ],
        #         resources=["*"]
        #     )
            
        #     function.add_to_role_policy(
        #         bedrock_policy
        #     )