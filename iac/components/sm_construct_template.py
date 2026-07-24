from aws_cdk import (
    aws_secretsmanager as secretsmanager,
)
import json
from constructs import Construct


# usado especialmente para segredos de assinatura de eventos no event bridge
# secrets manager é caro, então se for usar esse construct use com cuidado

class SmConstruct(Construct):
    event_secret: secretsmanager.ISecret

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        stack_name: str,
        stage: str,
        **kargs
    ):

        super().__init__(scope, construct_id, **kargs)

        stage = stage.lower()

        self.event_secret = secretsmanager.Secret(
            self,
            id="EventBridgeDeleteSecret",
            secret_name=f"{stack_name}/event-bridge-delete-secret/{stage}",
            description="Secret used to sign EventBridge delete trigger",
            generate_secret_string=secretsmanager.SecretStringGenerator(
                secret_string_template=json.dumps({"EVENT_SECRET": ""}),
                generate_string_key="EVENT_SECRET",
                password_length=64,
                exclude_punctuation=True
            )
        )
