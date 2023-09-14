from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from io import BufferedReader
from typing import List, Union

@dataclass
class MonetaryValues:
    purchased_at: Union[str, datetime]
    name: str
    amount: str
    installment_of: Union[str, None]
    installment_to: Union[str, None]

class IPDFParser(ABC):
    @abstractmethod
    def extract_expenses(self, 
                         buffered_pdf: BufferedReader) -> List[MonetaryValues]:
        ...