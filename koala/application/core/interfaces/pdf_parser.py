# built-in
from abc import ABC, abstractmethod
from datetime import datetime
from io import BufferedReader
from typing import List, Union
import re

# third-party
from pydantic import field_validator
from pydantic.dataclasses import dataclass

from koala.application.core.utils.transformers import Transformer

@dataclass
class MonetaryValues:
    """Data class to represent monetary values extracted from a PDF.

    Attributes:
        :purchased_at: It accepts A Union of str "YYYY-MM-DD" and datetime representing the date of purchase and returns the datetime representation of it.
        name: A string representing the name of the item or service purchased.
        amount: A string representing the amount spent.
        installment_of: A Union of str and None representing the current installment number.
        installment_to: A Union of str and None representing the total number of installments.
    """
    purchased_at: Union[str, datetime]
    name: str
    amount: float
    installment_of: Union[int, None]
    installment_to: Union[int, None]

    @field_validator("purchased_at", mode='before')
    def transform_purchased_at(cls, 
                               date: Union[str, datetime]) -> datetime:
        return Transformer.string_to_datetime(date=date)
    

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