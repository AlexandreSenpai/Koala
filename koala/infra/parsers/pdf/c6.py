from datetime import datetime
from io import BufferedReader
import logging
import re
from typing import List

import PyPDF2

from koala.infra.core.interfaces.pdf_parser import IPDFParser, MonetaryValues


class C6Parser(IPDFParser):

    def __init__(self, 
                 initial_costs_page: int = 2,
                 pdf_reader: PyPDF2 = PyPDF2) -> None:
        self._pdf_reader = pdf_reader
        self.initial_costs_page = initial_costs_page

    def get_pages(self, buffered_pdf: BufferedReader) -> List[str]:
        pdf = self._pdf_reader.PdfReader(buffered_pdf)
        return [page.extract_text() for page in pdf.pages[self.initial_costs_page:]]
    
    def replace_month_pt_to_en(self, date_str):
        pt_months = ('JAN', 'FEV', 'MAR', 'ABR', 'MAI', 'JUN', 'JUL', 'AGO', 'SET', 'OUT', 'NOV', 'DEZ')
        en_months = ('JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC')
        for pt, en in zip(pt_months, en_months):
            date_str = date_str.upper().replace(pt, en)
        return date_str
    
    def get_monetary_values(self, page: str) -> List[MonetaryValues]:
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
        pages = self.get_pages(buffered_pdf=buffered_pdf)
        
        expenses = []
        for page in pages:
            expenses.extend(self.get_monetary_values(page))

        return expenses
