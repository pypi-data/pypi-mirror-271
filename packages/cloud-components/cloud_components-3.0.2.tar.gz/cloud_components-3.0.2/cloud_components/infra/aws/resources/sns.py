import json
from typing import Any, Literal
from botocore.exceptions import ClientError
from cloud_components.application.interface.infra.event import IEvent
from cloud_components.application.interface.services.log.logger import ILogger


class Sns(IEvent):
    _source: str | None = None

    def __init__(self, connection: Any, logger: ILogger):
        self.connection = connection
        self.logger = logger

    @property
    def source(self) -> Any:
        if not self._source:
            raise ValueError("Source not found")
        return self._source

    @source.setter
    def source(self, value: str):
        self._source = value

    def send(
        self, message: dict, message_structere: Literal["json"] | None = None
    ) -> bool:
        self.logger.info(f"Sending message to {self.source}")
        try:
            if message_structere:
                self.connection.publish(
                    TargetArn=self.source,
                    Message=json.dumps({"default": json.dumps(message)}),
                    MessageStructure=message_structere,
                )
            else:
                self.connection.publish(
                    TargetArn=self.source,
                    Message=json.dumps(message),
                )
        except ClientError as err:
            self.logger.error(
                "An error occurred when try to send a message "
                + f"to {self.source}. Error detail: {err}"
            )
            return False
        return True
