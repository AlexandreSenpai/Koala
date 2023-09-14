# built-in
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from io import BufferedReader
from typing import List, Union

@dataclass
class MonetaryValues:
    """Data class to represent monetary values extracted from a PDF.

    Attributes:
        :purchased_at: A Union of str and datetime representing the date of purchase.
        name: A string representing the name of the item or service purchased.
        amount: A string representing the amount spent.
        installment_of: A Union of str and None representing the current installment number.
        installment_to: A Union of str and None representing the total number of installments.
    """
    purchased_at: Union[str, datetime]
    name: str
    amount: str
    installment_of: Union[str, None]
    installment_to: Union[str, None]

class IPDFParser(ABC):
    """Abstract base class for PDF parsers.

    This class defines the interface for extracting expenses from a PDF.
    """
    @abstractmethod
    def extract_expenses(self, 
                         buffered_pdf: BufferedReader) -> List[MonetaryValues]:
        """Abstract method to extract expenses from a PDF.

        Args:
            buffered_pdf: A buffered PDF file.

        Returns:
            A list of MonetaryValues objects representing the extracted expenses.
        """
        ...