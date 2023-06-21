from decimal import Decimal
from aws_cdk import (
    aws_dynamodb as dynamodb, RemovalPolicy,
)
from constructs import Construct


class TemplateDynamoTable(Construct):
    table: dynamodb.Table

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.table = dynamodb.Table(
            self, "TemplateDynamoTable",
            partition_key=dynamodb.Attribute(
                name="PK",
                type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(
                name="SK",
                type=dynamodb.AttributeType.STRING
            ), 
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY
        )
        
    


