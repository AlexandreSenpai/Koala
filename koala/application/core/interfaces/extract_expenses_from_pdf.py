from dataclasses import dataclass
from io import BufferedReader
from typing import List

from koala.application.core.interfaces.use_case import IUseCase
from koala.infra.core.interfaces.pdf_parser import IPDFParser, MonetaryValues

@dataclass
class ExtractExpensesFromPDFUseCaseRequestDTO:
    pdf_buffer: BufferedReader

@dataclass
class ExtractExpensesFromPDFUseCaseResponseDTO:
    expenses: List[MonetaryValues]

class IExtractExpensesFromPDF(IUseCase[ExtractExpensesFromPDFUseCaseRequestDTO, 
                                       ExtractExpensesFromPDFUseCaseResponseDTO]):
    def __init__(self, pdf_parser: IPDFParser) -> None:
        ...