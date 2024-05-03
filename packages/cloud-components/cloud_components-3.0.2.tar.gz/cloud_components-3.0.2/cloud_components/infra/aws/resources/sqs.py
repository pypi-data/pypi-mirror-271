from typing import Any
from botocore.exceptions import ClientError
from cloud_components.application.interface.infra.queue import IQueue
from cloud_components.application.interface.services.log.logger import ILogger


class Sqs(IQueue):
    _queue: str | None = None
    _queue_name: str | None = None

    def __init__(self, connection: Any, logger: ILogger) -> None:
        self.connection = connection
        self.logger = logger

    @property
    def queue(self) -> Any:
        if not self._queue:
            raise ValueError("Queue not found")
        return self._queue

    @queue.setter
    def queue(self, value: str):
        self._queue_name = value
        self._queue = self.connection.get_queue_by_name(QueueName=value)

    def send_message(self, message: str) -> bool:
        self.logger.info(f"Sending message to {self._queue_name} queue.")
        try:
            self.queue.send_message(MessageBody=message)
        except ClientError as err:
            self.logger.error(
                "An error occurred when try to send a message to"
                + f"{self._queue_name} queue. Error: {err}"
            )
            return False
        return True

    def receive_message(self) -> str:
        raise NotImplementedError
