# built-in
from datetime import datetime
import logging
import re
from typing import List

# parsers
from koala.application.parsers.pdf.default import DefaultParser

# interfaces
from koala.application.core.interfaces.pdf_parser import MonetaryValues
from koala.application.core.utils.date import Date


class NubankParser(DefaultParser):
    """Parser for extracting monetary values from Nubank PDFs.

    Attributes:
        initial_costs_page (int): The page number where the costs start in the PDF.
    """

    __EXPENSE_PATTERN = r"(\d{2} \w{3})\s*\n\s*\n([^\n]+)(?:\s+-\s+(\d+/\d+))?\s*\n([\d,]+)"
    
    def __init__(self, 
                 initial_costs_page: int = 3) -> None:
        """Initializes NubankParser with the given page number.

        Args:
            initial_costs_page: An integer indicating the page number where the costs
                information starts in the PDF. Defaults to 3.
        """
        super().__init__(initial_costs_page=initial_costs_page)

    def get_monetary_values(self, page: str) -> List[MonetaryValues]:
        """Extracts monetary values from a given PDF page.

        Args:
            page: A string containing the text content of a PDF page.

        Returns:
            A list of MonetaryValues objects representing the extracted monetary values.
        """
    
        matches = re.findall(self.__EXPENSE_PATTERN, page)

        expenses = []

        for date, name, _, value in matches:
            try:
                splitted_name = name.split('-')
                installment_of = splitted_name[-1].split('/')[0].strip() if len(splitted_name) > 1 else None
                installment_to = splitted_name[-1].split('/')[1].strip() if len(splitted_name) > 1 else None

                name = "-".join(splitted_name[:-1]).strip() if len(splitted_name) > 1 else splitted_name[0].strip()
                date = Date.replace_month_pt_to_numerical(date_str=f"{date} {datetime.now().year}")

                expenses.append(MonetaryValues(purchased_at=date,
                                               name=name,
                                               amount=value.replace(',', '.'),
                                               installment_of=installment_of,
                                               installment_to=installment_to))
            except Exception as err:
                logging.warn(f'Could not process an item. {err}')
                continue

        return expenses
