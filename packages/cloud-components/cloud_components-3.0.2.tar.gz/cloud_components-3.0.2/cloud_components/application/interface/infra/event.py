from abc import ABC, abstractmethod
from typing import Any, Literal


class IEvent(ABC):
    @property
    @abstractmethod
    def source(self) -> Any:
        raise NotImplementedError

    @source.setter
    @abstractmethod
    def source(self, value: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def send(self, message: dict, message_structere: Literal["json"] = "json") -> bool:
        raise NotImplementedError
