import sys
from koala.application.core.interfaces.use_case import DTO
from koala.application.use_cases.create_expense import CreateExpenseUseCase, CreateExpenseUseCaseRequestDTO
from koala.domain.entities.expense import ExpenseType

from koala.infra.core.interfaces.expense_repository import IExpensesRepository

sys.path.insert(0, '../')

import pytest

def describe_create_expense():
    # Mock the IExpensesRepository
    class MockExpensesRepository(IExpensesRepository):
        def create_expense(self, expense):
            expense.id = 1
            return expense

    class MockFailingExpensesRepository(IExpensesRepository):
        def create_expense(self, expense):
            return expense

    def test_create_expense_use_case_with_valid_data():
        # Arrange
        mock_repo = MockExpensesRepository()
        use_case = CreateExpenseUseCase(expenses_repository=mock_repo)

        request_dto = CreateExpenseUseCaseRequestDTO(
            name="Test Expense",
            purchased_at="2023-08-01",
            type=ExpenseType.FIXED,
            amount=100.0
        )

        # Act
        response_dto = use_case.execute(data=DTO[CreateExpenseUseCaseRequestDTO](data=request_dto))

        # Assert
        assert response_dto.id == 1
        assert response_dto.created is True

    def test_create_expense_use_case_with_invalid_data():
        # Arrange
        mock_repo = MockExpensesRepository()
        use_case = CreateExpenseUseCase(expenses_repository=mock_repo)


        # Act and Assert
        with pytest.raises(ValueError):
            request_dto = CreateExpenseUseCaseRequestDTO(
                name="",  # Invalid name
                purchased_at="2023-08-01",
                type=ExpenseType.FIXED,
                amount=100.0
            )
            use_case.execute(data=DTO(request_dto))

    def test_create_expense_use_case_with_failed_creation():
        # Arrange
        mock_repo = MockFailingExpensesRepository()
        use_case = CreateExpenseUseCase(expenses_repository=mock_repo)

        request_dto = CreateExpenseUseCaseRequestDTO(
            name="Test Expense",
            purchased_at="2023-08-01",
            type=ExpenseType.FIXED,
            amount=100.0
        )

        # Act
        response_dto = use_case.execute(data=DTO(request_dto))

        # Assert
        assert response_dto.id == 0
        assert response_dto.created is False