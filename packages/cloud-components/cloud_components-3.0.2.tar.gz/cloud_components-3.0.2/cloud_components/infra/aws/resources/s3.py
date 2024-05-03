from typing import Any
from botocore.exceptions import ClientError

from cloud_components.application.interface.services.log.logger import ILogger
from cloud_components.application.interface.infra.storage import IStorage


class S3(IStorage):
    """
    An implementation from IStorage interface, this class comunicate
    with Aws S3 service, and you can write and read archieves into
    any bucket.

    ...

    Attributes
    ----------
    connection : Any
        Instance of resource object from boto3
    logger : ILogger
        Logger object that share the same methods with ILogger
    env : IEnviroment
        Enviroment class instance
    bucket : Any
        Bucket object from boto3

    Parameters
    ----------
    connection : Any
        Instance of resource function from boto3
    logger : ILogger
        Logger object that share the same methods with ILogger
    env : IEnviroment
        Enviroment class instance

    Methods
    ----------
    save_file(data: str, file_path: str, content_type: str, is_public: bool = False) -> bool

    get_file(file_path: str) -> str | None
    """

    _bucket = None

    def __init__(self, connection: Any, logger: ILogger) -> None:
        self.connection = connection
        self.logger = logger

    @property
    def bucket(self) -> Any:
        return self._bucket

    @bucket.setter
    def bucket(self, name: str):
        self._bucket = self.connection.Bucket(name)

    def save_file(
        self,
        data: bytes,
        file_path: str,
        content_type: str,
        is_public: bool = False,
    ) -> bool:
        """
        Returns
        ----------
        bool
            return true when you can save a file, and false when occurs
        """
        try:
            if is_public:
                self.logger.info(
                    "Saving a file with public acl and "
                    + f"content-type as '{content_type}' in '{file_path}'"
                )
                self.bucket.put_object(
                    Key=file_path,
                    Body=data,
                    ACL="public-read",
                    ContentType=content_type,
                )
            else:
                self.logger.info(
                    f"Saving a file with content-type as '{content_type}' in '{file_path}'"
                )
                self.bucket.put_object(
                    Key=file_path, Body=data, ContentType=content_type
                )
        except ClientError as err:
            self.logger.error(
                f"An error occurred when try to save a file in S3. Error detail: {err}"
            )
            return False
        return True

    def get_file(self, file_path: str) -> bytes | None:
        self.logger.info(f"Getting file from '{file_path}'")
        try:
            content = self.bucket.Object(file_path)
            content = content.get()["Body"].read()
        except ClientError as err:
            self.logger.error(
                f"An error occurred when try to get a file in S3. Error detail: {err}"
            )
            return None
        return content

    def ls(self, path: str) -> list[str]:  # pylint: disable=C0103
        self.logger.info(f"Listing objects from {path}")
        return [_object.key for _object in self.bucket.objects.filter(Prefix=path)]

    def delete(self, file_path: str) -> bool:
        try:
            self.bucket.Object(file_path).delete()
        except Exception as err:  # pylint: disable=W0612,W0718
            return False
        return True
