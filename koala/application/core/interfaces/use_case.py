from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TypeVar, Generic

T = TypeVar('T')
V = TypeVar('V')

@dataclass
class DTO(Generic[T]):
    """Data Transfer Object (DTO) class.

    Generic data class to represent data transfer objects.

    Attributes:
        data: Generic type T representing the data to be transferred.
    """
    data: T

class IUseCase(Generic[T, V], ABC):
    """Abstract base class for use cases.

    This class defines the interface for executing a use case and is
    generic over the input and output types.

    Generic Types:
        T: The type of the input data.
        V: The type of the output data.
    """

    @abstractmethod
    def execute(self, data: DTO[T]) -> V:
        """Abstract method to execute the use case.

        Args:
            data: A DTO object containing the input data of type T.

        Returns:
            An object of type V representing the output of the use case.
        """
        pass