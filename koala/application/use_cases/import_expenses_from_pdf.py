# interfaces
from koala.application.core.interfaces.extract_expenses_from_pdf import (ExtractExpensesFromPDFUseCaseRequestDTO, 
                                                                         ExtractExpensesFromPDFUseCaseResponseDTO, 
                                                                         IExtractExpensesFromPDF)
from koala.application.core.interfaces.use_case import DTO
from koala.infra.core.interfaces.pdf_parser import IPDFParser


class ExtractExpensesFromPDFUseCase(IExtractExpensesFromPDF):
    """Implements the IExtractExpensesFromPDF interface.

    This class is responsible for extracting expenses from a PDF file and storing them.

    Attributes:
        _pdf_parser: An instance of a class that implements the IPDFParser interface.
    """
    def __init__(self, 
                 pdf_parser: IPDFParser) -> None:
        """Initializes ExtractExpensesFromPDFUseCase with a given PDF parser.

        Args:
            pdf_parser: An instance of a class that implements the IPDFParser interface.
        """
        self._pdf_parser = pdf_parser

    def execute(self, data: DTO[ExtractExpensesFromPDFUseCaseRequestDTO]) -> ExtractExpensesFromPDFUseCaseResponseDTO:
        """Executes the use case to extract expenses from a PDF.

        Args:
            data: A DTO object containing the request data.

        Returns:
            An ExtractExpensesFromPDFUseCaseResponseDTO object representing the response.
        """
        dto_data = data.data
        return ExtractExpensesFromPDFUseCaseResponseDTO(expenses=self._pdf_parser.extract_expenses(buffered_pdf=dto_data.pdf_buffer))

