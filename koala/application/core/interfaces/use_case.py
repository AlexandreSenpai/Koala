from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TypeVar

T = TypeVar('T')
V = TypeVar('V')

@dataclass
class DTO:
    data: T

class IUseCase(ABC):
    @abstractmethod
    def execute(self, data: DTO) -> V:
        pass