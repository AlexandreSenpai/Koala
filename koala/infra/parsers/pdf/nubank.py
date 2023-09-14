from datetime import datetime
from io import BufferedReader
import logging
import re
from typing import List

import PyPDF2

from koala.infra.core.interfaces.pdf_parser import IPDFParser, MonetaryValues


class NubankParser(IPDFParser):

    def __init__(self, 
                 initial_costs_page: int = 3,
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
            date_str = date_str.replace(pt, en)
        return date_str
    
    def get_monetary_values(self, page: str) -> List[MonetaryValues]:
        pattern = r"(\d{2} \w{3})\s*\n\s*\n([^\n]+)(?:\s+-\s+(\d+/\d+))?\s*\n([\d,]+)"
        matches = re.findall(pattern, page)

        expenses = []

        for date, name, _, value in matches:
            try:
                splitted_name = name.split('-')
                installment_of = splitted_name[-1].split('/')[0].strip() if len(splitted_name) > 1 else None
                installment_to = splitted_name[-1].split('/')[1].strip() if len(splitted_name) > 1 else None

                name = "-".join(splitted_name[:-1]).strip() if len(splitted_name) > 1 else splitted_name[0].strip()
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
