import boto3
from cloud_components.application.types.aws import ResourceType


class ConnectorFactory:
    """
    Manufacture connection type

    ...

    Methods
    ----------
    manufacture(resource: Literal["sqs", "dynamodb", "s3", "lambda"], **kwargs)
        Manufacture the connection based in resorce and can be a boto3.client
        or boto3.resource
    """

    @staticmethod
    def manufacture(resource: ResourceType, **kwargs):
        """
        Params
        ----------
        resource
            Can be any aws service
        kwargs
            Extra params to manufacture the connection

        Returns
        ----------
        Any
            boto3.client or boto3.resource
        """
        if resource in ["lambda", "sns"]:
            return boto3.client(resource, **kwargs)
        return boto3.resource(resource, **kwargs)
