# built-in
from dataclasses import dataclass
from io import BufferedReader
from typing import List

# interfaces
from koala.application.core.interfaces.use_case import IUseCase
from koala.application.core.interfaces.pdf_parser import IPDFParser, MonetaryValues

@dataclass
class ExtractExpensesFromPDFUseCaseRequestDTO:
    """Data class to represent the request for ExtractExpensesFromPDF use case.

    Attributes:
        pdf_buffer: A buffered PDF file.
    """
    pdf_buffer: BufferedReader

@dataclass
class ExtractExpensesFromPDFUseCaseResponseDTO:
    """Data class to represent the response for ExtractExpensesFromPDF use case.

    Attributes:
        expenses: A list of MonetaryValues objects representing the extracted expenses.
    """
    expenses: List[MonetaryValues]

class IExtractExpensesFromPDF(IUseCase[ExtractExpensesFromPDFUseCaseRequestDTO, 
                                       ExtractExpensesFromPDFUseCaseResponseDTO]):
    """Interface for the ExtractExpensesFromPDF use case.

    This class defines the interface for extracting expenses from a PDF and
    extends from the IUseCase interface.

    Attributes:
        pdf_parser: An instance of a class that implements the IPDFParser interface.
    """
    def __init__(self, pdf_parser: IPDFParser) -> None:
        """Initializes the IExtractExpensesFromPDF interface.

        Args:
            pdf_parser: An instance of a class that implements the IPDFParser interface.
        """
        ...