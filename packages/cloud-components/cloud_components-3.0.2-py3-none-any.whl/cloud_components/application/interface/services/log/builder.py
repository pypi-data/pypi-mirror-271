from abc import ABC, abstractmethod

from cloud_components.application.interface.services.log.logger import ILogger


class ILogBuilder(ABC):
    @abstractmethod
    def build_loguru(self) -> ILogger:
        raise NotImplementedError
