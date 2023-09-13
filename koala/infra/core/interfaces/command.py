from abc import ABC, abstractmethod

class ICommand(ABC):
    @abstractmethod
    def run(self) -> None:
        ...