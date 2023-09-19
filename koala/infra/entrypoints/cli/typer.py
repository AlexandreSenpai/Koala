# third-party
import typer

# use-cases
from koala.application.use_cases.create_expense import CreateExpenseUseCase
from koala.application.use_cases.extract_expenses_from_pdf import ExtractExpensesFromPDFUseCase

# parsers
from koala.application.parsers.pdf.c6 import C6Parser
from koala.application.parsers.pdf.nubank import NubankParser

# interfaces
from koala.infra.core.interfaces.command import ICommand

# adapters
from koala.infra.adapters.database.sqlite import SQLite
from koala.infra.adapters.database.sqlite.models.base import Base
from koala.infra.adapters.repositories.expenses import ExpensesRepository
from koala.infra.core.utils.path import Path

# commands
from koala.infra.entrypoints.cli.commands.create_expense import CreateExpenseCommand
from koala.infra.entrypoints.cli.commands.import_expenses_by_pdf import ImportExpenses

def init_database() -> SQLite:
    """Initialize the SQLite database and create all necessary tables.
    
    Returns:
        SQLite: An instance of the SQLite database.
    """

    connection_string = f"sqlite:///{Path.join(__file__, '../../adapters/database/sqlite/koala.sqlite')}"
    database = SQLite(connection_str=connection_string)
    Base.metadata.create_all(database._engine)
    return database

def register_command(name: str, 
                     command: ICommand, 
                     cli: typer.Typer) -> None:
    """Register a command to the CLI.
    
    Args:
        name: The name of the command.
        command: The command instance.
        cli: The Typer CLI instance.
        
    Returns:
        None: None if successful, raises an Exception otherwise.
    """
    if isinstance(command, ICommand):
        cli.command(name=name)(command.run)
        return
    
    raise Exception(f'You can only register instances of {ICommand}.')


def create_cli() -> None:
    """Main function to create the Command Line Interface (CLI)."""

    cli = typer.Typer()
    with init_database() as database:
        if database._session is None:
            raise Exception('Could not open a valid database session.')
        
        expenses_repository = ExpensesRepository(session=database._session)
        create_expense_use_case = CreateExpenseUseCase(expenses_repository=expenses_repository)

        register_command(name='create-expense', 
                         command=CreateExpenseCommand(create_expense_use_case=create_expense_use_case), 
                         cli=cli)

        import_expenses = ImportExpenses(create_expense_use_case=create_expense_use_case)
        import_expenses.add_extractor(name='nubank',
                                      extractor=ExtractExpensesFromPDFUseCase(pdf_parser=NubankParser()))
        import_expenses.add_extractor(name='c6',
                                      extractor=ExtractExpensesFromPDFUseCase(pdf_parser=C6Parser()))

        register_command(name='import-expenses', 
                         command=import_expenses, 
                         cli=cli)
        
        cli()