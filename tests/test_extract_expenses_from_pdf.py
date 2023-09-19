import sys

sys.path.insert(0, '../')

import pytest
from koala.application.core.interfaces.extract_expenses_from_pdf import ExtractExpensesFromPDFUseCaseRequestDTO

from koala.application.core.interfaces.pdf_parser import IPDFParser, MonetaryValues
from koala.application.core.interfaces.use_case import DTO
from koala.application.use_cases.extract_expenses_from_pdf import ExtractExpensesFromPDFUseCase
from unittest.mock import Mock

def describe_extract_expense_from_pdf():
        # Mock para IPDFParser
    class MockPDFParser(IPDFParser):
        def extract_expenses(self, buffered_pdf):
            return ["despesa1", "despesa2"]

    def test_extract_expenses_from_pdf_use_case_with_valid_data():
        # Arrange (Preparação)
        mock_parser = MockPDFParser()
        use_case = ExtractExpensesFromPDFUseCase(pdf_parser=mock_parser)

        request_dto = ExtractExpensesFromPDFUseCaseRequestDTO(pdf_buffer="algum_buffer_pdf")

        # Act (Ação)
        response_dto = use_case.execute(data=DTO(request_dto))

        # Assert (Verificação)
        assert len(response_dto.expenses) == 2
        assert response_dto.expenses[0] == "despesa1"
        assert response_dto.expenses[1] == "despesa2"

    def test_extract_expenses_from_pdf_use_case_with_no_expenses():
        # Arrange (Preparação)
        mock_parser = Mock(spec=IPDFParser)
        mock_parser.extract_expenses.return_value = [MonetaryValues(purchased_at='2023-01-01', name='teste', amount=100.4)]
        use_case = ExtractExpensesFromPDFUseCase(pdf_parser=mock_parser)

        request_dto = ExtractExpensesFromPDFUseCaseRequestDTO(pdf_buffer="algum_buffer_pdf")

        # Act (Ação)
        response_dto = use_case.execute(data=DTO(request_dto))

        # Assert (Verificação)
        assert len(response_dto.expenses) == 1
        assert isinstance(response_dto.expenses[0], MonetaryValues)