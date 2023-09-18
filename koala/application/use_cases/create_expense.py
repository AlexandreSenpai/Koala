# built-in
from datetime import datetime
from typing import Optional, Union, cast

# third-party
from pydantic.dataclasses import dataclass
from pydantic import field_validator

# interfaces
from koala.application.core.interfaces.use_case import DTO, IUseCase
from koala.application.core.utils.transformers import Transformer
from koala.domain.entities.expense import Expense, ExpenseType
from koala.infra.core.interfaces.expense_repository import IExpensesRepository

@dataclass
class CreateExpenseUseCaseRequestDTO:
    """Data class to represent the request for CreateExpenseUseCase.

    Attributes:
        name: A string representing the name of the expense.
        purchased_at: A string representing the date of purchase.
        type: An ExpenseType enum representing the type of expense.
        amount: A float representing the amount spent.
        installment_of: An optional integer representing the current installment number.
        installment_to: An optional integer representing the total number of installments.
    """
    name: str
    purchased_at: Union[datetime, str]
    type: ExpenseType
    amount: float
    installment_of: Optional[Union[int, str]] = None
    installment_to: Optional[Union[int, str]] = None

    @field_validator('purchased_at', mode='before')
    def transform_purchased_at(cls, 
                               date: Union[datetime, str]) -> datetime:
        return Transformer.string_to_datetime(date=date)

    @field_validator('installment_of', mode='before')
    def transform_installment_of(cls, 
                                 installment: Union[None, str, int]) -> Union[int, None]:
        return int(installment) if installment is not None else None
    
    @field_validator('name', mode='before')
    def validate_name(cls, 
                      name: str) -> str:
        if not name:
            raise ValueError('You must provide a valid expense name.')
        return name

@dataclass
class CreateExpenseUseCaseResponseDTO:
    """Data class to represent the response for CreateExpenseUseCase.

    Attributes:
        id: A Union of str and int representing the ID of the created expense.
        created: A boolean indicating whether the expense was successfully created.
    """
    id: Union[str, int]
    created: bool

class CreateExpenseUseCase(IUseCase):
    """Implements the CreateExpenseUseCase interface.

    This class is responsible for creating an expense and storing it in the repository.

    Attributes:
        _expenses_repository: An instance of a class that implements the IExpensesRepository interface.
    """

    def __init__(self, 
                 expenses_repository: IExpensesRepository) -> None:
        """Initializes CreateExpenseUseCase with a given expenses repository.

        Args:
            expenses_repository: An instance of a class that implements the IExpensesRepository interface.
        """
        self._expenses_repository: IExpensesRepository = expenses_repository
    
    def execute(self, data: DTO[CreateExpenseUseCaseRequestDTO]) -> CreateExpenseUseCaseResponseDTO:
        """Executes the use case to create an expense.

        Args:
            data: A DTO object containing the request data.

        Returns:
            A CreateExpenseUseCaseResponseDTO object representing the response.
        """
        expense_data = data.data
        date: datetime = cast(datetime, expense_data.purchased_at)
        expense = Expense(purchased_at=date,
                          amount=expense_data.amount,
                          name=expense_data.name,
                          type=expense_data.type,
                          installment_of=cast(int, expense_data.installment_of),
                          installment_to=cast(int, expense_data.installment_to))
        
        expense = self._expenses_repository.create_expense(expense=expense)

        return CreateExpenseUseCaseResponseDTO(id=expense.id,
                                               created=True if expense.id != 0 else False)


