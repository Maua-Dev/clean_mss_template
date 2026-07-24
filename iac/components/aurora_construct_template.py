# iac/contructs/aurora_construct.py
from aws_cdk import (
    RemovalPolicy, Duration,
    aws_ec2 as ec2,
    aws_rds as rds,
    aws_secretsmanager as secretsmanager,
)
from constructs import Construct


RETAINED_STAGES = {"prod", "homolog"}


class AuroraConstruct(Construct):
    
    cluster: rds.DatabaseCluster
    secret: secretsmanager.ISecret
    default_database_name: str
    vpc: ec2.IVpc

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        stack_name: str,
        stage: str,
        **kargs
    ) -> None:

        super().__init__(scope, construct_id, **kargs)

        stage = stage.lower()

        removal = RemovalPolicy.RETAIN if stage in RETAINED_STAGES else RemovalPolicy.DESTROY
        
        # aurora exige uma vpc - não é necessario criar endpoints para lambda ou secrets manager (cuidado com o custo)

        vpc = ec2.Vpc(
            self,
            id="Vpc",
            vpc_name=f"{stack_name}-Vpc-{stage}",
            max_azs=2,
            ip_addresses=ec2.IpAddresses.cidr("10.0.0.0/16"),
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="PrivateSubnet",
                    subnet_type=ec2.SubnetType.PRIVATE_ISOLATED,
                    cidr_mask=24
                )
            ],
            nat_gateways=0
        )
        
        # senha do bd armazenada no SM
        
        # recomendo no futuro fortemente trocar isso por uma simples senha pré configurada, sem depender de secrets manager
        # por que? secrets manager é caro e não precisamos de tamanha "segurança"

        creds = rds.Credentials.from_generated_secret(
            username="app_user",
            # muda o template_mss quando estiver diferenciando do template
            secret_name=f"/template_mss/aurora/{stage}/credentials"
        )

        # muda isso quando estiver diferenciando
        db_name = "template_database_name"

        self.cluster = rds.DatabaseCluster(
            self,
            id="AuroraCluster",
            cluster_identifier=f"{stack_name}-AuroraCluster-{stage}".lower(),
            engine=rds.DatabaseClusterEngine.aurora_postgres(
                version=rds.AuroraPostgresEngineVersion.VER_16_8
            ),
            writer=rds.ClusterInstance.serverless_v2(
                "WriterInstance",
                scale_with_writer=True,
            ),
            
            # essa instancia do aurora escala para 0. Se voce que for editar aqui a infra mudar esse min capacity pra algo diferente de 0
            # saiba que a AWS vai te cobrar por volta de 30 dolares por mes no minimo que voce pode colocar (..min_capacity=0.5)
            
            # escalar pra 0 tem um cold start de algo por volta de 20 segundos - fique atento ao tempo de timeout setado na lambda

            serverless_v2_min_capacity=0,
            serverless_v2_max_capacity=2,
            default_database_name=db_name,
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(
                subnet_type=ec2.SubnetType.PRIVATE_ISOLATED
            ),
            credentials=creds,
            removal_policy=removal,
            enable_data_api=True,
            backup=rds.BackupProps(
                retention=Duration.days(5)
            ),
        )

        self.secret = self.cluster.secret
        self.default_database_name = db_name
        self.vpc = vpc