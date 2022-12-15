import enum
from enum import Enum
import os

from src.shared.domain.repositories.user_repository_interface import IUserRepository


class STAGE(Enum):
    DOTENV = "DOTENV"
    DEV = "DEV"
    PROD = "PROD"
    TEST = "TEST"


class Environments:
    """
    Defines the environment variables for the application. You should not instantiate this class directly. Please use Environments.get_envs() method instead.

    Usage:

    """
    stage: STAGE
    s3_bucket_name: str

    def _configure_local(self):
        from dotenv import load_dotenv
        os.environ["STAGE"] = STAGE.DOTENV.value
        load_dotenv()

    def load_envs(self):
        if "STAGE" not in os.environ or os.environ["STAGE"] == STAGE.DOTENV.value:
            self._configure_local()

        self.stage = STAGE[os.environ.get("STAGE")]

        if self.stage == STAGE.TEST:
            self.s3_bucket_name = "bucket-test"

        else:
            self.s3_bucket_name = os.environ.get("S3_BUCKET_NAME")


    @staticmethod
    def get_user_repo() -> IUserRepository:
        if Environments.get_envs().stage == STAGE.TEST:
            from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock
            return UserRepositoryMock
        # elif Environments.get_envs().stage == STAGE.PROD:
        #     from src.shared.infra.repositories.user_repository_dynamo import UserRepositoryDynamo
        #     return UserRepositoryDynamo
        # else:
        #     from src.shared.infra.repositories.user_repository_dynamo import UserRepositoryDynamo
        #     return UserRepositoryDynamo

    @staticmethod
    def get_envs() -> "Environments":
        """
        Returns the Environments object. This method should be used to get the Environments object instead of instantiating it directly.
        :return: Environments (stage={self.stage}, s3_bucket_name={self.s3_bucket_name}, region={self.region}, endpoint_url={self.endpoint_url})

        """
        envs = Environments()
        envs.load_envs()
        return envs

    def __repr__(self):
        return self.__dict__

