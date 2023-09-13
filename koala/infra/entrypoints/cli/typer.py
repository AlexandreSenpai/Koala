# built-in
from typing import Union

# third-party
import typer

# use-cases
from koala.application.use_cases.create_expense import CreateExpenseUseCase

# interfaces
from koala.infra.core.interfaces.command import ICommand

# adapters
from koala.infra.adapters.database.sqlite import SQLite
from koala.infra.adapters.database.sqlite.models.base import Base
from koala.infra.adapters.repositories.expenses import ExpensesRepository
from koala.infra.core.utils.path import Path
from koala.infra.entrypoints.cli.commands.create_expense import CreateExpenseCommand

def init_database() -> SQLite:
    """Initialize the SQLite database and create all necessary tables.
    
    Returns:
        SQLite: An instance of the SQLite database.
    """

    connection_string = f"sqlite:///{Path.join(__file__, '../../adapters/database/sqlite/koala.sqlite')}"
    database = SQLite(connection_str=connection_string)
    Base.metadata.create_all(database._engine)
    return database

def register_command(name: str, command: ICommand, cli: typer.Typer, ) -> Union[None, Exception]:
    if isinstance(command, ICommand):
        cli.command(name=name)(command.run)
        return
    
    raise Exception(f'You can only register instances of {ICommand}.')


def create_cli() -> None:
    """Main function to create the Command Line Interface (CLI)."""

    cli = typer.Typer()
    with init_database() as database:
        expenses_repository = ExpensesRepository(session=database._session)
        create_expense_use_case = CreateExpenseUseCase(expenses_repository=expenses_repository)

        register_command(name='create-expense', 
                         command=CreateExpenseCommand(create_expense_use_case=create_expense_use_case), 
                         cli=cli)
        
        cli()