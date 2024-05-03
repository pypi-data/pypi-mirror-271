from abc import ABC, abstractmethod


class ILogger(ABC):  # pylint: disable=C0115
    @abstractmethod
    def debug(self, message: str) -> None:  # pylint: disable=C0116
        raise NotADirectoryError

    @abstractmethod
    def info(self, message: str) -> None:  # pylint: disable=C0116
        raise NotADirectoryError

    @abstractmethod
    def success(self, message: str) -> None:  # pylint: disable=C0116
        raise NotADirectoryError

    @abstractmethod
    def warning(self, message: str) -> None:  # pylint: disable=C0116
        raise NotADirectoryError

    @abstractmethod
    def error(self, message: str) -> None:  # pylint: disable=C0116
        raise NotADirectoryError
