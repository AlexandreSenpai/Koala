# built-in
from typing import cast

# third-party
from sqlalchemy.orm import Session

# entities
from koala.domain.entities.expense import Expense

# models
from koala.infra.adapters.database.sqlite.models.expense import Expense as ExpenseModel

# interfaces
from koala.infra.core.interfaces.expense_repository import IExpensesRepository

class ExpensesRepository(IExpensesRepository):
    """Implements the IExpensesRepository interface for SQLite databases.

    This class is responsible for managing Expense entities in a SQLite database.

    Attributes:
        _session: A Session object for the SQLite database.
    """

    def __init__(self, 
                 session: Session) -> None:
        """Initializes ExpensesRepository with a given SQLAlchemy session.

        Args:
            session: A Session object for the SQLite database.
        """
        self._session = session

    def create_expense(self, 
                       expense: Expense) -> Expense:
        """Creates a new Expense entity in the SQLite database.

        Args:
            expense: An Expense entity to be created in the database.

        Returns:
            The created Expense entity with its ID updated.
        """
        model = ExpenseModel(purchased_at=expense.purchased_at,
                             name=expense.name,
                             type=expense.type.value,
                             amount=expense.amount,
                             installment_of=expense.installment_of,
                             installment_to=expense.installment_to)
        self._session.add(model)
        self._session.commit()
        expense.id = cast(int, model.id)
        return expense