# built-in
from datetime import datetime
from enum import Enum
import logging
from typing import Dict, List, Literal

# third-party
from PyInquirer import prompt
import typer
from rich import print, console, table
from koala.application.core.interfaces.extract_expenses_from_pdf import (ExtractExpensesFromPDFUseCaseRequestDTO, 
                                                                         IExtractExpensesFromPDF)
from koala.application.core.interfaces.use_case import DTO, IUseCase
from koala.application.use_cases.create_expense import CreateExpenseUseCaseRequestDTO
from koala.domain.entities.expense import ExpenseType

# entities

# use-cases

# interfaces
from koala.infra.core.interfaces.command import ICommand
from koala.infra.core.interfaces.pdf_parser import MonetaryValues

class AvailableExtractors(Enum):
    """Enum for available PDF extractors."""
    NUBANK = 'nubank'
    C6 = 'c6'

class ImportExpenses(ICommand):
    """Command class for importing expenses from PDF.

    This class is responsible for handling the command-line interface for importing expenses.

    Attributes:
        __extractors: A dictionary mapping extractor names to their instances.
        _create_expense_use_case: A use case for creating expenses.
    """
    def __init__(self,
                 create_expense_use_case: IUseCase) -> None:
        self.__extractors: Dict[str, IExtractExpensesFromPDF] = {}
        self._create_expense_use_case = create_expense_use_case
    
    def add_extractor(self, 
                      name: str, 
                      extractor: IExtractExpensesFromPDF) -> bool:
        """Adds a new extractor to the list of available extractors.

        Args:
            name: The name of the extractor.
            extractor: The extractor instance.

        Returns:
            bool: True if the extractor was added, False otherwise.
        """
        if name in self.__extractors:
            logging.warn('Could not add extractor because it already exists.')
            return False
        self.__extractors[name] = extractor
        return True
    
    def get_extractor(self, name: AvailableExtractors) -> IExtractExpensesFromPDF:
        """Retrieves an extractor by its name.

        Args:
            name: The name of the extractor.

        Returns:
            IExtractExpensesFromPDF: The extractor instance.

        Raises:
            Exception: If the extractor was not found.
        """
        if name.value in self.__extractors:
            return self.__extractors[name.value]
        
        raise Exception('This extractor was not added.')

    def get_extractor_from_client(self) -> IExtractExpensesFromPDF:
        """Prompts the user to select an extractor.

        Returns:
            IExtractExpensesFromPDF: The selected extractor instance.

        Raises:
            Exception: If an invalid option was selected.
        """
        extractor_question = [{ 
            'type': 'list',
            'name': 'extractor',
            'message': 'Select the Available Provider',
            'choices': [extractor.name.capitalize() for extractor in AvailableExtractors]
        }]
        
        extractor_answer: Dict[Literal["extractor"], str] = prompt(extractor_question)
        try:
            extractor_name = AvailableExtractors[extractor_answer['extractor'].upper()]
            return self.get_extractor(name=extractor_name)
        except KeyError:
            raise Exception('Invalid extractor option.')
    
    def get_import_confirmation_from_client(self, expenses: List[MonetaryValues]) -> bool:
        """Prompts the user for confirmation to import expenses.

        Args:
            expenses: The list of expenses to be imported.

        Returns:
            bool: True if the user confirms, False otherwise.
        """
        print(f"[bold yellow]You are going to import {len(expenses)} expenses.[/bold yellow]")
        
        output_table = table.Table("Index", 
                                   "Purchased At", 
                                   "Name", 
                                   "Installment Of", 
                                   "Installment To", 
                                   "Amount")
        for i, expense in enumerate(expenses):
            date = datetime.strftime(expense.purchased_at, '%d/%m/%Y') \
                if isinstance(expense.purchased_at, datetime) \
                else expense.purchased_at
            
            output_table.add_row(str(i+1),
                                 date, 
                                 expense.name, 
                                 expense.installment_of, 
                                 expense.installment_to, 
                                 expense.amount)
        
        console.Console().print(output_table)

        confirmation: str = typer.prompt("Confirm [Y/N]")
        if confirmation.lower() == 'y':
            return True
        
        return False

    def get_file_path_from_client(self) -> str:
        """Prompts the user for the file path of the PDF to import.

        Returns:
            str: The file path provided by the user.
        """
        return typer.prompt("Bank bill ABSOLUTE file path")
    
    def get_expense_type(self) -> ExpenseType:
        """Prompts the user to select the type of expense.

        Returns:
            ExpenseType: The type of expense selected by the user.
        """
        type_question = [{ 
            'type': 'list',
            'name': 'type',
            'message': 'Expense Type',
            'choices': [ExpenseType.FIXED.value, 
                        ExpenseType.VARIABLE.value]
        }]
        
        type_answer = prompt(type_question)

        convert_str_to_enum = {
            'variable': ExpenseType.VARIABLE,
            'installment': ExpenseType.INSTALLMENT,
            'fixed': ExpenseType.FIXED
        }

        return convert_str_to_enum[type_answer['type']]
    
    def create_expenses(self, expenses: List[MonetaryValues]) -> None:
        """Creates expenses based on the extracted data.

        Args:
            expenses: The list of expenses to be created.
        """
        for expense in expenses:
            expense_type = ExpenseType.INSTALLMENT
            if expense.installment_of is None:
                print(f"Expense Name: {expense.name} that cost [bold red]{expense.amount}[/bold red].")
                expense_type = self.get_expense_type()
    
            data = CreateExpenseUseCaseRequestDTO(name=expense.name,
                                                  purchased_at=expense.purchased_at,
                                                  amount=float(expense.amount),
                                                  installment_of=expense.installment_of,
                                                  installment_to=expense.installment_to,
                                                  type=expense_type)
            
            self._create_expense_use_case.execute(data=DTO(data=data))
        
    def run(self) -> None:
        """Executes the command to import and create expenses.

        This method runs the command-line interface for importing and creating expenses.
        """
        provider = self.get_extractor_from_client()
        expenses: List[MonetaryValues] = []

        while True:
            try:
                with open(self.get_file_path_from_client(), 'rb') as pdf:
                    extracted_expenses = provider.execute(data=DTO(data=ExtractExpensesFromPDFUseCaseRequestDTO(pdf_buffer=pdf)))
                    expenses.extend(extracted_expenses.expenses)
                    pdf.close()
                break
            except FileNotFoundError:
                logging.error('Was not possible to find the bank bill file by the provided file path.')
            except IsADirectoryError:
                logging.error('The provided file path heads to a directory.')
            except Exception as err:
                logging.error(f'Could not open the provided file. {err}')
# 
        confirmed = self.get_import_confirmation_from_client(expenses=expenses)

        if confirmed:
            self.create_expenses(expenses=expenses)
        
        print('[bold green]Expenses Created Successfully![/bold green]')
        

    
        