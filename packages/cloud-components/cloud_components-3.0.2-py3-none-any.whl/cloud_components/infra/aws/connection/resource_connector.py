from typing import Literal
from cloud_components.infra.aws.connection.connector_factory import ConnectorFactory
from cloud_components.application.interface.services.log.logger import ILogger
from cloud_components.application.types.aws import ResourceType


class ResourceConnector:
    """
    This class create a connection with AWS and created to be
    used in all service implementations

    ...

    Attributes
    ----------
    logger : ILogger
        Logger object that share the same methods with ILogger
    env : IEnviroment
        Enviroment class instance

    Methods
    ----------
    connect(self, resource_name: ResourceType)
        Build a connection resource or connection client from boto3 using a
        connector factory
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
        self.access_key = access_key
        self.secret_access_key = secret_access_key
        self.localstack_url = localstack_url
        self.env = env

    def connect(self, resource_name: ResourceType):
        """
        Params
        ----------
        resource_name
            Can be any aws service

        Returns
        ----------
        Any:
            An object from boto3.resource or boto3.client based in resource name
        """
        if self.env == "local" and self.localstack_url:
            self.logger.info(f"Connecting to {resource_name} at local enviroment")
            return ConnectorFactory.manufacture(
                resource=resource_name,
                aws_access_key_id=self.access_key,
                aws_secret_access_key=self.secret_access_key,
                endpoint_url=self.localstack_url,
            )
        if self.env == "local" and not self.localstack_url:
            self.logger.info(f"Connecting to {resource_name}")
            return ConnectorFactory.manufacture(
                resource=resource_name,
                aws_access_key_id=self.access_key,
                aws_secret_access_key=self.secret_access_key,
            )
        self.logger.info(f"Connecting to {resource_name}")
        return ConnectorFactory.manufacture(
            resource=resource_name,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_access_key,
        )
