from abc import ABC, abstractmethod
from typing import Generic, TypeVar

Connection = TypeVar('Connection')

class IDatabase(Generic[Connection], ABC):
    """Abstract base class for Database objects.

    This class defines the interface for all Database objects in the application.

    Attributes:
        _connection_str: A string representing the database connection string.

    Methods:
        connect: Abstract method that must be implemented by subclasses to establish a database connection.
        disconnect: Abstract method that must be implemented by subclasses to close a database connection.
    """

    def __init__(self, connection_str: str) -> None:
        """Initializes IDatabase with a given connection string.

        Args:
            connection_str: A string representing the database connection string.
        """
        self._connection_str: str = connection_str

    @abstractmethod
    def connect(self) -> Connection:
        """Abstract method to establish a database connection.

        This method should be implemented by subclasses to provide the logic for establishing a database connection.

        Returns:
            A Connection object representing the database connection.
        """
        ...

    @abstractmethod
    def disconnect(self) -> bool:
        """Abstract method to close a database connection.

        This method should be implemented by subclasses to provide the logic for closing a database connection.

        Returns:
            A boolean indicating whether the disconnection was successful.
        """
        ...
