# built-in
from datetime import datetime
from io import BufferedReader
import logging
import re
from typing import List

# third-party
import PyPDF2

# interfaces
from koala.infra.core.interfaces.pdf_parser import IPDFParser, MonetaryValues


class C6Parser(IPDFParser):
    """Parses PDF files from C6 Bank to extract financial information.

    Attributes:
        initial_costs_page: An integer indicating the page number where the costs
            information starts in the PDF.
    """
    def __init__(self, 
                 initial_costs_page: int = 2) -> None:
        """Initializes C6Parser with the given page number.

        Args:
            initial_costs_page: An integer indicating the page number where the costs
                information starts in the PDF. Defaults to 2.
        """
        self.initial_costs_page = initial_costs_page

    def get_pages(self, buffered_pdf: BufferedReader) -> List[str]:
        """Extracts text from the PDF pages starting from `initial_costs_page`.

        Args:
            buffered_pdf: A buffered PDF file.

        Returns:
            A list of strings, each representing the text content of a PDF page.
        """
        pdf = PyPDF2.PdfReader(buffered_pdf)
        return [page.extract_text() for page in pdf.pages[self.initial_costs_page:]]
    
    def replace_month_pt_to_en(self, date_str):
        """Replaces Portuguese month abbreviations with English ones in a date string.

        Args:
            date_str: A string containing a date with Portuguese month abbreviations.

        Returns:
            A string containing the date with English month abbreviations.
        """
        pt_months = ('JAN', 'FEV', 'MAR', 'ABR', 'MAI', 'JUN', 'JUL', 'AGO', 'SET', 'OUT', 'NOV', 'DEZ')
        en_months = ('JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC')
        for pt, en in zip(pt_months, en_months):
            date_str = date_str.upper().replace(pt, en)
        return date_str
    
    def get_monetary_values(self, page: str) -> List[MonetaryValues]:
        """Extracts monetary values from a given PDF page.

        Args:
            page: A string containing the text content of a PDF page.

        Returns:
            A list of MonetaryValues objects representing the extracted monetary values.
        """
        pattern = r"(\d{2} \w{3}) ([\w\s\*]+)(?: - Parcela (\d+\/\d+))? (\d+,\d+)"
        matches = re.findall(pattern, page)

        expenses = []

        for date, name, installments, value in matches:
            try:
                installments = installments if installments != "" else None
                installment_of = installments.split('/')[0] if installments else None
                installment_to = installments.split('/')[1] if installments else None

                date = self.replace_month_pt_to_en(f"{date} {datetime.now().year}")
                expenses.append(MonetaryValues(purchased_at=datetime.strptime(date, "%d %b %Y"),
                                               name=name,
                                               amount=str(value.replace(',', '.')),
                                               installment_of=installment_of,
                                               installment_to=installment_to))
            except Exception as err:
                logging.warn(f'Could not process an item. {err}')
                continue

        return expenses
            

    def extract_expenses(self, 
                         buffered_pdf: BufferedReader) -> List[MonetaryValues]:
        """Extracts all expenses from the PDF.

        Args:
            buffered_pdf: A buffered PDF file.

        Returns:
            A list of MonetaryValues objects representing all extracted expenses.
        """
        pages = self.get_pages(buffered_pdf=buffered_pdf)
        
        expenses = []
        for page in pages:
            expenses.extend(self.get_monetary_values(page))

        return expenses
