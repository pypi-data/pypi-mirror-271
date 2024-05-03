from abc import ABC, abstractmethod

from cloud_components.application.interface.infra.storage import IStorage
from cloud_components.application.interface.infra.function import IFunction
from cloud_components.application.interface.infra.queue import IQueue
from cloud_components.application.interface.infra.event import IEvent


class IBuilder(ABC):  # pylint: disable=C0115
    @abstractmethod
    def build_storage(self) -> IStorage:  # pylint: disable=C0116
        raise NotImplementedError

    @abstractmethod
    def build_function(self) -> IFunction:
        raise NotImplementedError

    @abstractmethod
    def build_queue(self) -> IQueue:
        raise NotImplementedError

    @abstractmethod
    def build_event(self) -> IEvent:
        raise NotImplementedError
