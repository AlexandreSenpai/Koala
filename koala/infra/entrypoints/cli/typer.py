# built-in
from datetime import datetime
from typing import List, Tuple

# third-party
from dateutil.relativedelta import relativedelta
from PyInquirer import prompt
import typer
from rich import print

# interfaces
from koala.application.core.interfaces.use_case import DTO, IUseCase

# use-cases
from koala.application.use_cases.create_expense import (CreateExpenseUseCase, 
                                                        CreateExpenseUseCaseRequestDTO, 
                                                        CreateExpenseUseCaseResponseDTO)

# entities
from koala.domain.entities.expense import ExpenseType

# adapters
from koala.infra.adapters.database.sqlite import SQLite
from koala.infra.adapters.database.sqlite.models.base import Base
from koala.infra.adapters.repositories.expenses import ExpensesRepository
from koala.infra.core.interfaces.command import ICommand
from koala.infra.core.utils.path import Path

__cli = typer.Typer()

def init_database():
    connection_string = f"sqlite:///{Path.join(__file__, '../../adapters/database/sqlite/koala.sqlite')}"
    database = SQLite(connection_str=connection_string)
    Base.metadata.create_all(database._engine)
    return database

class CreateExpenseCommand(ICommand):
    def __init__(self, 
                 create_expense_use_case: IUseCase) -> None:
        self._create_expense_use_case = create_expense_use_case

    def get_installment_type(self) -> ExpenseType:
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
        name = typer.prompt('Expense name')
        purchased_at = typer.prompt('Purchased at')

        type = self.get_installment_type()

        expenses: List[Tuple[int, str]] = []
        installment_of = None
        installment_to = None

        if type == ExpenseType.INSTALLMENT:
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
                                               type=type,
                                               amount=amount,
                                               installment_of=expense[0],
                                               installment_to=installment_to) for expense in expenses]
        
    def run(self) -> None:
        print(f'[bold yellow]Welcome to expense creator.[/bold yellow]')
        while True:
            try:
                for expense in self.create_expenses_data():
                    created: CreateExpenseUseCaseResponseDTO = self._create_expense_use_case.execute(DTO(data=expense))
                    print(f'[bold green]Created {expense.name} expense with id "{created.id}" successfully![/bold green]')
                typer.echo('\n')
            except KeyboardInterrupt:
                break


def create_cli() -> typer.Typer:
    with init_database() as database:
        expenses_repository = ExpensesRepository(session=database._session)
        create_expense_use_case = CreateExpenseUseCase(expenses_repository=expenses_repository)
        create_expense_command = CreateExpenseCommand(create_expense_use_case=create_expense_use_case)

        __cli.command()(create_expense_command.run)

        return __cli()