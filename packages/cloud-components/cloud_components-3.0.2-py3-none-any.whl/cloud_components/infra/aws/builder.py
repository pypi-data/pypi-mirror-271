from typing import Literal
from cloud_components.application.interface.infra.event import IEvent
from cloud_components.application.interface.infra.function import IFunction
from cloud_components.application.interface.infra.queue import IQueue
from cloud_components.application.types.aws import ResourceType
from cloud_components.infra.aws.connection.resource_connector import ResourceConnector
from cloud_components.application.interface.infra.builder import IBuilder
from cloud_components.application.interface.infra.storage import IStorage
from cloud_components.application.interface.services.log.logger import ILogger
from cloud_components.infra.aws.resources.lambda_function import Lambda
from cloud_components.infra.aws.resources.s3 import S3
from cloud_components.infra.aws.resources.sqs import Sqs
from cloud_components.infra.aws.resources.sns import Sns


class AwsBuilder(IBuilder):
    """
    An implementation of IBuilder interface and responsible
    to build resource implementation, like S3, SQS, and many
    other services.

    ...

    Attributes
    ----------
    logger : ILogger
        Logger object that share the same methods with ILogger
    env : IEnviroment
        Enviroment class instance

    Methods
    ----------
    build_storage()
        Instanciate the S3 class with a connection instance from s3
        service
    """

    def __init__(
        self,
        logger: ILogger,
        access_key: str,
        secret_access_key: str,
        env: Literal["local"] | None = None,
        localstack_url: str | None = None,
    ) -> None:
        self.logger = logger
        self.resource = ResourceConnector(
            self.logger, access_key, secret_access_key, env, localstack_url
        )

    def _set_connection(self, resource_name: ResourceType):
        self.logger.info(f"Building {resource_name} implementation")
        return self.resource.connect(resource_name=resource_name)

    def build_storage(self) -> IStorage:
        """
        Returns
        ----------
        IStorage
            An instance of S3 class, and a implementation from IStorage
            interface
        """
        return S3(
            connection=self._set_connection(resource_name="s3"), logger=self.logger
        )

    def build_function(self) -> IFunction:
        return Lambda(
            connection=self._set_connection(resource_name="lambda"), logger=self.logger
        )

    def build_queue(self) -> IQueue:
        return Sqs(
            connection=self._set_connection(resource_name="sqs"), logger=self.logger
        )

    def build_event(self) -> IEvent:
        return Sns(
            connection=self._set_connection(resource_name="sns"), logger=self.logger
        )
