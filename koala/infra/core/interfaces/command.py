from abc import ABC, abstractmethod

class ICommand(ABC):
    """Abstract base class for Command objects.

    This class defines the interface for all Command objects in the application.

    Methods:
        run: Abstract method that must be implemented by subclasses to execute the command.
    """
    @abstractmethod
    def run(self) -> None:
        """Abstract method to execute the command.

        This method should be implemented by subclasses to provide the logic for executing the command.

        Returns:
            None
        """
        ...