from aws_cdk import aws_apigateway as apigateway
from constructs import Construct
from aws_cdk.aws_apigateway import (
    Cors,
    CorsOptions,
    GatewayResponse,
    Resource,
    ResponseType,
    RestApi,
)


class ApigwConstruct(Construct):
    
    rest_api: RestApi
    api_gateway_resource: Resource

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        stack_name: str,
        stage: str,
        **kwargs
    ):
        super().__init__(scope, construct_id, **kwargs)

        stage = stage.lower()
        
        # quando estiver diferenciando do template, remove o cors.ALL_ORIGINS e coloca, em prod, os endpoints do route 53 determinados
        # pelo front
        # em dev e homolog (seguindo o if else) coloca os endpoints para teste E os endpoints do route 53 para tais ambientes (dev e hml)

        cors_options = CorsOptions(
            allow_origins = Cors.ALL_ORIGINS
                # endpoints do route 53
                # [
                #     "https://reservation.maua.br",
                #     "https://reservation.devmaua.com"
                # ] 
            if stage == 'PROD'
            else 
                Cors.ALL_ORIGINS,
                # [
                #     "https://reservation.hml.devmaua.com",
                #     "https://reservation.dev.devmaua.com",
                #     "https://localhost:3000",
                #     "http://localhost:3000"
                # ],
            allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            allow_headers=Cors.DEFAULT_HEADERS
        )

        self.rest_api = RestApi(
            self,
            id="RestApi",
            rest_api_name=f"{stack_name}-RestApi-{stage}",
            description=f"{stack_name} RestApi for {stage}",
            deploy_options=apigateway.StageOptions(
                stage_name=stage,
                logging_level=apigateway.MethodLoggingLevel.OFF,
                data_trace_enabled=False,
                metrics_enabled=True,
                tracing_enabled=True,
            ),
            default_cors_preflight_options=cors_options,
        )
        
        self.api_gateway_resource = self.rest_api.root.add_resource(
            # troca isso quando criar um novo projeto
            # é a extensão que aparece no link das apis https://link-api/template-mss ; https://link-api/pe-mss ; https://link-api/reservation-api
            path_part="template-mss",
            default_cors_preflight_options=cors_options
        )
        
        # configurações de default response para casos de deny do authorizer (provavelmente pq não possui interface lambda response)
                
        GatewayResponse(
            self,
            "AuthorizerDenyResponse",
            rest_api=self.rest_api,
            type=ResponseType.ACCESS_DENIED,
            response_headers={
                "Access-Control-Allow-Origin": "'*'",
                "Access-Control-Allow-Headers": "'*'",
                "Access-Control-Allow-Methods": "'*'",
            },
            status_code="403"
        )
        
        GatewayResponse(
            self,
            "AuthorizerUnauthorizedResponse",
            rest_api=self.rest_api,
            type=ResponseType.UNAUTHORIZED,
            response_headers={
                "Access-Control-Allow-Origin": "'*'",
                "Access-Control-Allow-Headers": "'*'",
                "Access-Control-Allow-Methods": "'*'",
            },
            status_code="401"
        )