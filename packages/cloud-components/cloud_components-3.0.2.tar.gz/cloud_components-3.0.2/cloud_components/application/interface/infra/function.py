from abc import ABC, abstractmethod


class IFunction(ABC):
    @property
    @abstractmethod
    def function(self):
        raise NotImplementedError

    @abstractmethod
    def execute(self, payload: bytes):
        raise NotImplementedError
