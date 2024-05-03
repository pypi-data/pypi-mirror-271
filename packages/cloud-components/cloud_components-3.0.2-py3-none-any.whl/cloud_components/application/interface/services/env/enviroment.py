from abc import ABC, abstractmethod
from typing import Any, Callable


class IEnviroment(ABC):  # pylint: disable=C0115
    @abstractmethod
    def load(self) -> None:  # pylint: disable=C0116
        raise NotImplementedError

    @abstractmethod
    def get(  # pylint: disable=C0116
        self,
        env_name: str,
        cast: Callable[[Any], Any] | None = None,
        defalt: Any | None = None,
    ) -> Any:
        raise NotImplementedError
