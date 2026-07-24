from constructs import Construct
from aws_cdk import Resource, aws_ssm as ssm
from aws_cdk.aws_apigateway import RestApi
from aws_cdk import aws_s3 as s3

# usado especialmente para passar variáveis de ambiente para o front
# fique atento, no deploy do front existe um step ( se nao existir, adicione ) para pegar essas variaveis
# e coloca-las no ambiente do front, devemos sempre manter isso em mente para evitar discrepâncias
# o caminho passado no CD para pegar, por exemplo, o endpoint da api é determinado por esse construct

class SsmConstruct(Construct):

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        stage: str,
        mss_name_identification_for_path: str,
        api: RestApi,
        api_gateway_resource: Resource,
        buckets: dict[str, s3.Bucket] = None,
        extra_params: dict[str, str] = None,
        **kwargs
    ):
        super().__init__(scope, construct_id, **kwargs)
        
        # é necessário a '/' após a url pois no CD do front estamos contando como se ela ja estivesse la

        # stage lower é necessário aqui pois no actions do front, stage é recebido como lower
        
        stage = stage.lower()
        
        mss_name_identification_for_path = mss_name_identification_for_path.lower().replace("-", "_")

        if api:
            ssm.StringParameter(self,
                id=f"ApiUrl_{stage}",
                parameter_name=f"/{mss_name_identification_for_path}/{stage}/api/url",
                string_value=f"{api.url}{api_gateway_resource.path.lstrip('/')}/"
            )

        for logical_name, bucket in (buckets or {}).items():
            ssm.StringParameter(self,
                id=f"Bucket_{logical_name}_{stage}",
                parameter_name=f"/{mss_name_identification_for_path}/{stage}/buckets/{logical_name}",
                string_value=bucket.bucket_name
            )

        for key, value in (extra_params or {}).items():
            safe_id = key.replace("/", "_")
            ssm.StringParameter(self,
                id=f"Extra_{safe_id}_{stage}",
                parameter_name=f"/{mss_name_identification_for_path}/{stage}/{key}",
                string_value=value
            )