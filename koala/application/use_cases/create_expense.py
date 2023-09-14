from dataclasses import dataclass
from datetime import datetime
from koala.application.core.interfaces.use_case import DTO, IUseCase
from koala.domain.entities.expense import Expense, ExpenseType
from koala.infra.core.interfaces.expense_repository import IExpensesRepository

@dataclass
class CreateExpenseUseCaseRequestDTO:
    name: str
    purchased_at: str
    type: ExpenseType
    amount: float
    installment_of: int = None
    installment_to: int = None

@dataclass
class CreateExpenseUseCaseResponseDTO:
    id: str
    created: bool

class CreateExpenseUseCase(IUseCase):
    def __init__(self, 
                 expenses_repository: IExpensesRepository) -> None:
        self._expenses_repository: IExpensesRepository = expenses_repository
    
    def execute(self, data: DTO) -> CreateExpenseUseCaseResponseDTO:
        expense_data: CreateExpenseUseCaseRequestDTO = data.data
        date = datetime.strptime(expense_data.purchased_at, '%Y-%m-%d') \
            if isinstance(expense_data.purchased_at, str) \
            else expense_data.purchased_at

        expense = Expense(purchased_at=date,
                          amount=expense_data.amount,
                          name=expense_data.name,
                          type=expense_data.type,
                          installment_of=expense_data.installment_of,
                          installment_to=expense_data.installment_to)
        
        expense = self._expenses_repository.create_expense(expense=expense)

        return CreateExpenseUseCaseResponseDTO(id=expense.id,
                                               created=True)


