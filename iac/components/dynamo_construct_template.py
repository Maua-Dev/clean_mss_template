from aws_cdk import (
    RemovalPolicy,
    aws_dynamodb as dynamodb,
)
from constructs import Construct

# Mantenha alinhado com src.shared.infra.external.dynamo.template_table1_naming.TEMPLATE_TABLE1_PREFIX
_TEMPLATE_TABLE1_PREFIX = "TemplateTable1"

RETAINED_STAGES = {"prod", "homolog"}


class DynamoConstruct(Construct):

    template_table1: dynamodb.Table

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        stack_name: str,
        stage: str,
        **kwargs,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        stage_lower = stage.lower()

        removal_policy = (
            RemovalPolicy.RETAIN if stage_lower in RETAINED_STAGES else RemovalPolicy.DESTROY
        )

        self.template_table1 = dynamodb.Table(
            self,
            id="TemplateTable1",
            partition_key=dynamodb.Attribute(
                name="pk",
                type=dynamodb.AttributeType.STRING,
            ),
            sort_key=dynamodb.Attribute(
                name="sk",
                type=dynamodb.AttributeType.STRING,
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=removal_policy,
            table_name=f"{_TEMPLATE_TABLE1_PREFIX}-{stage_lower}",
            point_in_time_recovery_specification=dynamodb.PointInTimeRecoverySpecification(
                point_in_time_recovery_enabled=(stage_lower == "prod")
            ),
        )