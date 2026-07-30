import enum
from enum import Enum
import os
from src.shared.domain.observability.observability_interface import IObservability

from src.shared.domain.repositories.item_repository_interface import IItemRepository
from src.shared.domain.repositories.user_repository_interface import IUserRepository


class STAGE(Enum):
    DOTENV = "DOTENV"
    DEV = "DEV"
    HOMOLOG = "HOMOLOG"
    PROD = "PROD"
    TEST = "TEST"


class Environments:
    """
    Defines the environment variables for the application. You should not instantiate this class directly. Please use Environments.get_envs() method instead.

    Usage:

    """
    # essenciais
    stage: STAGE
    region: str
    dynamo_table_name: str
    dynamo_partition_key: str
    dynamo_sort_key: str
    dynamo_endpoint_url: str = None  # DynamoDB Local (ex: http://localhost:8000); None na AWS
    mss_name: str
    # essenciais

    s3_template_bucket1_name: str

    def _configure_local(self):
        from dotenv import load_dotenv
        load_dotenv()
        os.environ["STAGE"] = os.environ.get("STAGE") or STAGE.DOTENV.value

    def load_envs(self):
        if "STAGE" not in os.environ or os.environ["STAGE"] == STAGE.DOTENV.value:
            self._configure_local()

        self.stage = STAGE[os.environ.get("STAGE")]
        self.mss_name = os.environ.get("MSS_NAME")

        if self.stage == STAGE.TEST:
            self.region = "sa-east-1"
            self.dynamo_table_name = "user_mss_template-table"
            self.dynamo_partition_key = "pk"
            self.dynamo_sort_key = "sk"
            self.dynamo_endpoint_url = "http://localhost:8000"
            # alinhe com nome do bucket no minIO
            self.s3_template_bucket1_name = "template_bucket1_name"

        else:
            # todas essas variáveis vem de ENVIRONMENT_VARIABLES em iac_stack.py
            self.region = os.environ.get("REGION")
            self.dynamo_table_name = os.environ.get("DYNAMO_TABLE_NAME")
            self.dynamo_partition_key = os.environ.get("DYNAMO_PARTITION_KEY")
            self.dynamo_sort_key = os.environ.get("DYNAMO_SORT_KEY")
            # só setar se usar DynamoDB Local/compatível fora da AWS; em Lambda real fica None
            self.dynamo_endpoint_url = os.environ.get("DYNAMO_ENDPOINT_URL")
            self.s3_template_bucket1_name = os.environ.get("S3_TEMPLATE_BUCKET1_NAME")

    @staticmethod
    def get_item_repo() -> IItemRepository:
        if Environments.get_envs().stage == STAGE.TEST:
            from src.shared.infra.repositories.item_repository_mock import ItemRepositoryMock
            return ItemRepositoryMock
        elif Environments.get_envs().stage in [STAGE.DEV, STAGE.HOMOLOG, STAGE.PROD]:
            from src.shared.infra.repositories.item_repository_dynamo import ItemRepositoryDynamo
            return ItemRepositoryDynamo
        else:
            raise Exception("No repository found for this stage")

    @staticmethod
    def get_user_repo() -> IUserRepository:
        if Environments.get_envs().stage == STAGE.TEST:
            from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock
            return UserRepositoryMock
        elif Environments.get_envs().stage in [STAGE.DEV, STAGE.HOMOLOG, STAGE.PROD]:
            from src.shared.infra.repositories.user_repository_dynamo import UserRepositoryDynamo
            return UserRepositoryDynamo
        else:
            raise Exception("No user repository found for this stage")

    @staticmethod
    def get_observability() -> IObservability:
        if Environments.get_envs().stage == STAGE.TEST:
            from src.shared.infra.external.observability.observability_mock import ObservabilityMock
            return ObservabilityMock
        elif Environments.get_envs().stage in [STAGE.DEV, STAGE.HOMOLOG, STAGE.PROD]:
            from src.shared.infra.external.observability.observability_aws import ObservabilityAWS
            return ObservabilityAWS
        else:
            raise Exception("No observability class found for this stage")
    @staticmethod
    def get_envs() -> "Environments":
        """
        Returns the Environments object. This method should be used to get the Environments object instead of instantiating it directly.
        :return: Environments (stage={self.stage}, region={self.region}, dynamo_table_name={self.dynamo_table_name}, dynamo_endpoint_url={self.dynamo_endpoint_url})

        """
        envs = Environments()
        envs.load_envs()
        return envs

    def __repr__(self):
        return self.__dict__

