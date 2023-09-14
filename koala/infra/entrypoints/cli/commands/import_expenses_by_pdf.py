# built-in
from datetime import datetime
from enum import Enum
import logging
from typing import Dict, List, Literal, Union

# third-party
from PyInquirer import prompt
import typer
from rich import print, console, table
from koala.application.core.interfaces.use_case import DTO, IUseCase
from koala.application.use_cases.create_expense import CreateExpenseUseCaseRequestDTO
from koala.domain.entities.expense import ExpenseType

# entities

# use-cases

# interfaces
from koala.infra.core.interfaces.command import ICommand
from koala.infra.core.interfaces.pdf_parser import IPDFParser, MonetaryValues

class AvailableParsers(Enum):
    NUBANK = 'nubank'
    C6 = 'c6'

class ImportExpenses(ICommand):
    def __init__(self,
                 create_expense_use_case: IUseCase) -> None:
        self.__parsers: Dict[str, IPDFParser] = {}
        self._create_expense_use_case = create_expense_use_case
    
    def add_parser(self, name: str, parser: IPDFParser) -> bool:
        if name in self.__parsers:
            logging.warn('Could not add parser because it already exists.')
            return False
        self.__parsers[name] = parser
        return True
    
    def get_parser(self, name: AvailableParsers) -> Union[IPDFParser, Exception]:
        if name.value in self.__parsers:
            return self.__parsers[name.value]
        
        raise Exception('This parser was not added.')

    def get_provider_from_client(self) -> IPDFParser:

        provider_question = [{ 
            'type': 'list',
            'name': 'parser',
            'message': 'Select the Available Provider',
            'choices': [parser.name.capitalize() for parser in AvailableParsers]
        }]
        
        provider_answer: Dict[Literal["parser"], str] = prompt(provider_question)
        try:
            parser_name = AvailableParsers[provider_answer['parser'].upper()]
            return self.get_parser(name=parser_name)
        except KeyError:
            raise Exception('Invalid provider option.')
    
    def get_import_confirmation_from_client(self, expenses: List[MonetaryValues]) -> bool:
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
        return typer.prompt("Bank bill ABSOLUTE file path")
    
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
    
    def create_expenses(self, expenses: List[MonetaryValues]) -> None:
        for expense in expenses:
            expense_type = ExpenseType.INSTALLMENT
            if expense.installment_of is None:
                print(f"Expense Name: {expense.name} that cost [bold red]{expense.amount}[/bold red].")
                expense_type = self.get_expense_type()
    
            data = CreateExpenseUseCaseRequestDTO(name=expense.name,
                                                  purchased_at=expense.purchased_at,
                                                  amount=expense.amount,
                                                  installment_of=expense.installment_of,
                                                  installment_to=expense.installment_to,
                                                  type=expense_type)
            
            self._create_expense_use_case.execute(data=DTO(data=data))
        
    def run(self) -> None:
        provider = self.get_provider_from_client()
        expenses: List[MonetaryValues] = []

        while True:
            try:
                with open(self.get_file_path_from_client(), 'rb') as pdf:
                    expenses.extend(provider.extract_expenses(buffered_pdf=pdf))
                    pdf.close()
                break
            except FileNotFoundError:
                logging.error('Was not possible to find the bank bill file by the provided file path.')
            except IsADirectoryError:
                logging.error('The provided file path heads to a directory.')
            except Exception as err:
                logging.error(f'Could not open the provided file. {err}')

        confirmed = self.get_import_confirmation_from_client(expenses=expenses)

        if confirmed:
            self.create_expenses(expenses=expenses)
        
        print('[bold green]Expenses Created Successfully![/bold green]')
        

    
        