from abc import ABC, abstractmethod

from koala.domain.entities.expense import Expense


class IExpensesRepository(ABC):
    @abstractmethod
    def create_expense(self, expense: Expense) -> Expense: ...