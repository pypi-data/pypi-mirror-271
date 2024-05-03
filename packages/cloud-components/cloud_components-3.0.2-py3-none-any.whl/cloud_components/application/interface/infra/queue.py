from abc import ABC, abstractmethod
from typing import Any


class IQueue(ABC):
    @property
    @abstractmethod
    def queue(self) -> Any:
        raise NotImplementedError

    @queue.setter
    @abstractmethod
    def queue(self, value: str):
        raise NotImplementedError

    @abstractmethod
    def send_message(self, message: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def receive_message(self) -> str:
        raise NotImplementedError
