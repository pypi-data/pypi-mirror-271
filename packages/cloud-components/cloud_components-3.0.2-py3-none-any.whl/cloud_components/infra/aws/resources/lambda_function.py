from typing import Any
from cloud_components.application.interface.infra.function import IFunction
from cloud_components.application.interface.services.log.logger import ILogger


class Lambda(IFunction):
    _name: str | None = None

    def __init__(self, connection: Any, logger: ILogger) -> None:
        self.connection = connection
        self.logger = logger

    @property
    def function(self):
        if not self._name:
            raise ValueError("You cannot call a function without a name")
        return self._name

    @function.setter
    def function(self, value: str):
        self._name = value

    def execute(self, payload: bytes):
        self.logger.info("Executing lambda...")
        raise NotImplementedError
