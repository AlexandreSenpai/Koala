# built-in
from datetime import datetime
from typing import List, Tuple

# third-party
from dateutil.relativedelta import relativedelta
from PyInquirer import prompt
import typer
from rich import print

# entities
from koala.domain.entities.expense import ExpenseType

# use-cases
from koala.application.use_cases.create_expense import (CreateExpenseUseCaseRequestDTO, 
                                                        CreateExpenseUseCaseResponseDTO)

# interfaces
from koala.application.core.interfaces.use_case import DTO, IUseCase
from koala.infra.core.interfaces.command import ICommand


class CreateExpenseCommand(ICommand):
    """Command class for creating expenses."""

    def __init__(self, 
                 create_expense_use_case: IUseCase) -> None:
        """Initializes the CreateExpenseCommand class.
        
        Args:
            create_expense_use_case (IUseCase): A use case for creating expenses.
        """
        self._create_expense_use_case = create_expense_use_case

    def get_expense_type(self) -> ExpenseType:
        """Prompts the user to select the type of installment for the expense.
        
        Returns:
            ExpenseType: The type of expense selected by the user.
        """
        type_question = [{ 
            'type': 'list',
            'name': 'type',
            'message': 'Expense Type',
            'choices': [ExpenseType.INSTALLMENT.value, 
                        ExpenseType.FIXED.value, 
                        ExpenseType.VARIABLE.value]
        }]
        
        type_answer = prompt(type_question)

        convert_str_to_enum = {
            'variable': ExpenseType.VARIABLE,
            'installment': ExpenseType.INSTALLMENT,
            'fixed': ExpenseType.FIXED
        }

        return convert_str_to_enum[type_answer['type']]
    
    def create_expenses_data(self) -> List[CreateExpenseUseCaseRequestDTO]:
        """Creates expense data based on user input.
        
        Returns:
            List[CreateExpenseUseCaseRequestDTO]: A list of DTOs containing expense data.
        """

        name = typer.prompt('Expense name')
        purchased_at = typer.prompt('Purchased at')

        expense_type = self.get_expense_type()

        expenses: List[Tuple[int, str]] = []
        installment_of = None
        installment_to = None

        if expense_type == ExpenseType.INSTALLMENT:
            installment_of = typer.prompt('Installment of')
            installment_to = typer.prompt('Installment to')
            
            for i, month in enumerate(range(int(installment_of)-1, int(installment_to))):
                date = datetime.strptime(purchased_at, '%Y-%m-%d') + relativedelta(months=month)
                expenses.append((int(installment_of) + i, date.strftime('%Y-%m-%d')))
        else:
            expenses.append((None, purchased_at))

        amount = typer.prompt('Expense amount')

        return [CreateExpenseUseCaseRequestDTO(name=name,
                                               purchased_at=expense[1],
                                               type=expense_type,
                                               amount=amount,
                                               installment_of=expense[0],
                                               installment_to=installment_to) for expense in expenses]
        
    def run(self) -> None:
        """Executes the command to create expenses."""

        print(f'[bold yellow]Welcome to expense creator.[/bold yellow]')
        while True:
            try:
                for expense in self.create_expenses_data():
                    created: CreateExpenseUseCaseResponseDTO = self._create_expense_use_case.execute(DTO(data=expense))
                    print(f'[bold green]Created {expense.name} expense with id "{created.id}" successfully![/bold green]')
                typer.echo('\n')
            except KeyboardInterrupt:
                break