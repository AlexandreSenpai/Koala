from abc import ABC, abstractmethod

from koala.domain.entities.expense import Expense


class IExpensesRepository(ABC):
    """Abstract base class for ExpensesRepository objects.

    This class defines the interface for all ExpensesRepository objects in the application.

    Methods:
        create_expense: Abstract method that must be implemented by subclasses to create an Expense entity.
    """

    @abstractmethod
    def create_expense(self, expense: Expense) -> Expense: 
        """Abstract method to create an Expense entity.

        This method should be implemented by subclasses to provide the logic for creating an Expense entity.

        Args:
            expense: An Expense entity to be created.

        Returns:
            The created Expense entity.
        """
        ...