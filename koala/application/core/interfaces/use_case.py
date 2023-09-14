from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TypeVar, Generic

T = TypeVar('T')
V = TypeVar('V')

@dataclass
class DTO(Generic[T]):
    data: T

class IUseCase(Generic[T, V], ABC):
    @abstractmethod
    def execute(self, data: DTO[T]) -> V:
        pass