from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
)
from constructs import Construct

from .template_dynamo_table import TemplateDynamoTable


class TemplateStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.dynamo_table = TemplateDynamoTable(self, "TemplateDynamoTable")

