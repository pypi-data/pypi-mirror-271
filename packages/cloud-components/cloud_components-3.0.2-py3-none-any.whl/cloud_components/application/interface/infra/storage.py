from abc import ABC, abstractmethod
from typing import Any


class IStorage(ABC):
    @abstractmethod
    def save_file(
        self,
        data: str,
        file_path: str,
        content_type: str,
        is_public: bool = False,
    ) -> bool:
        raise NotImplementedError

    @abstractmethod
    def get_file(self, file_path: str) -> str | None:
        raise NotImplementedError

    @property
    @abstractmethod
    def bucket(self) -> Any:
        raise NotImplementedError

    @bucket.setter
    @abstractmethod
    def bucket(self, name: str):
        raise NotImplementedError

    @abstractmethod
    def ls(self, path: str) -> list[str]:  # pylint: disable=C0103
        raise NotImplementedError

    @abstractmethod
    def delete(self, file_path: str) -> bool:
        raise NotImplementedError
