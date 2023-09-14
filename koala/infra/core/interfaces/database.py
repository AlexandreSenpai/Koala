from abc import ABC, abstractmethod
from typing import Generic, TypeVar

Connection = TypeVar('Connection')

class IDatabase(Generic[Connection], ABC):

    def __init__(self, connection_str: str) -> None:
        self._connection_str: str = connection_str

    @abstractmethod
    def connect(self) -> Connection:
        ...

    @abstractmethod
    def disconnect(self) -> bool:
        ...
