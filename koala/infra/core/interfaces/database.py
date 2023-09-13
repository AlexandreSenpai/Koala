from abc import ABC, abstractmethod
from typing import TypeVar

Connection = TypeVar('Connection')

class IDatabase(ABC):

    def __init__(self, connection_str: str) -> None:
        self._connection_str: str = connection_str

    @abstractmethod
    def connect(self) -> Connection:
        ...

    @abstractmethod
    def disconnect(self) -> bool:
        ...
