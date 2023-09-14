from koala.application.core.interfaces.extract_expenses_from_pdf import (ExtractExpensesFromPDFUseCaseRequestDTO, 
                                                                         ExtractExpensesFromPDFUseCaseResponseDTO, 
                                                                         IExtractExpensesFromPDF)
from koala.application.core.interfaces.use_case import DTO
from koala.infra.core.interfaces.pdf_parser import IPDFParser


class ExtractExpensesFromPDFUseCase(IExtractExpensesFromPDF):
    def __init__(self, 
                 pdf_parser: IPDFParser) -> None:
        self._pdf_parser = pdf_parser

    def execute(self, data: DTO[ExtractExpensesFromPDFUseCaseRequestDTO]) -> ExtractExpensesFromPDFUseCaseResponseDTO:
        dto_data: ExtractExpensesFromPDFUseCaseRequestDTO = data.data
        return ExtractExpensesFromPDFUseCaseResponseDTO(expenses=self._pdf_parser.extract_expenses(buffered_pdf=dto_data.pdf_buffer))

