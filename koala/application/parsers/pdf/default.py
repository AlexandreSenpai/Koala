# built-in
from io import BufferedReader, BytesIO
from typing import List, Union

# third-party
import pypdf

# interfaces
from koala.application.core.interfaces.pdf_parser import IPDFParser, MonetaryValues

class DefaultParser(IPDFParser):
    """Default parser for extracting monetary values from PDFs.

    Attributes:
        initial_costs_page (int): The page number where the costs start in the PDF.
    """

    def __init__(self, 
                 initial_costs_page: int = 3) -> None:
        """Initializes NubankParser with the given page number.

        Args:
            initial_costs_page: An integer indicating the page number where the costs
                information starts in the PDF. Defaults to 3.
        """
        self.initial_costs_page = initial_costs_page

    def get_pages(self, 
                  buffered_pdf: Union[BufferedReader, BytesIO],
                  initial_page: Union[int, None] = None) -> List[str]:
        """Extracts text from the PDF pages starting from `initial_costs_page`.

        Args:
            buffered_pdf: A buffered PDF file.

        Returns:
            A list of strings, each representing the text content of a PDF page.
        """
        initial_page = initial_page if initial_page is not None else self.initial_costs_page
        pdf = pypdf.PdfReader(buffered_pdf)
        
        if len(pdf.pages) < initial_page:
            raise Exception('Initial page is over the maximum pages of the pdf.')
        
        return [page.extract_text() for page in pdf.pages[initial_page:]]
    
    def get_monetary_values(self, page: str) -> List[MonetaryValues]:
        raise Exception('Not implemented Error')

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
