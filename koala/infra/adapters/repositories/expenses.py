from koala.domain.entities.expense import Expense
from koala.infra.adapters.database.sqlite.models.expense import Expense as ExpenseModel
from koala.infra.core.interfaces.expense_repository import IExpensesRepository
from sqlalchemy.orm import Session

class ExpensesRepository(IExpensesRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def create_expense(self, expense: Expense) -> Expense:
        model = ExpenseModel(purchased_at=expense.purchased_at,
                             name=expense.name,
                             type=expense.type.value,
                             amount=expense.amount,
                             installment_of=expense.installment_of,
                             installment_to=expense.installment_to)
        self._session.add(model)
        self._session.commit()
        expense.id = model.id
        return expense