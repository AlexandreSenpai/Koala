# built-in
from datetime import datetime
from os import path

# third-party
from dateutil.relativedelta import relativedelta
from PyInquirer import prompt
import typer

# interfaces
from koala.application.core.interfaces.use_case import DTO

# use-cases
from koala.application.use_cases.create_expense import CreateExpenseUseCase, CreateExpenseUseCaseRequestDTO

# entities
from koala.domain.entities.expense import ExpenseType

# adapters
from koala.infra.adapters.database.sqlite import SQLite
from koala.infra.adapters.database.sqlite.models.base import Base
from koala.infra.adapters.repositories.expenses import ExpensesRepository
from koala.infra.core.utils.path import Path

cli = typer.Typer()


connection_string = f"sqlite:///{Path.join(__file__, '../../adapters/database/sqlite/koala.sqlite')}"

with SQLite(connection_str=connection_string) as database:
    Base.metadata.create_all(database._engine)

    @cli.command(name='add_expense')
    def add_expense() -> None:
        repository = ExpensesRepository(session=database._session)
        create_expense_use_case = CreateExpenseUseCase(expenses_repository=repository)

        def create_expense(name: str, 
                           purchased_at: datetime, 
                           type: ExpenseType,
                           amount: float,
                           installment_of: int,
                           installment_to: int) -> None:
            data = CreateExpenseUseCaseRequestDTO(name=name,
                                                purchased_at=purchased_at,
                                                type=type,
                                                amount=amount,
                                                installment_of=installment_of,
                                                installment_to=installment_to)
                    
            expense = create_expense_use_case.execute(DTO(data=data))

            typer.echo(f'Created {name} expense successfully! id: {expense.id}\n')
        
        typer.echo(f'Welcome to expense creator. To exit press Ctrl + C')
        
        while True:
            try:
                purchased_at = typer.prompt('Purchased At')
                name = typer.prompt('Expense name')
                
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
                next_installments = [[None, purchased_at]]
                if (type := convert_str_to_enum[type_answer['type']]) == ExpenseType.INSTALLMENT:
                    installment_of = typer.prompt('Installment of')
                    installment_to = typer.prompt('Installment to')
                    next_installments[0][0] = installment_of
                    for month in range(int(installment_of), int(installment_to)):
                        date = datetime.strptime(purchased_at, '%Y-%m-%d') + relativedelta(months=month)
                        next_installments.append([int(installment_of) + month, date.strftime('%Y-%m-%d')])
                else:
                    installment_to = None
                    installment_of = None
                
                amount = typer.prompt('Expense amount')

                for installment in next_installments:
                    installment_of, purchased_at = installment
                    create_expense(name=name,
                                    amount=amount,
                                    type=type,
                                    installment_of=installment_of,
                                    installment_to=installment_to,
                                    purchased_at=purchased_at)
            except KeyboardInterrupt:
                break