import sys

from koala.infra.core.interfaces.expense_repository import IExpensesRepository

sys.path.insert(0, '../')

import pytest
from unittest.mock import MagicMock, Mock, patch
from sqlalchemy.orm import Session
from koala.infra.adapters.database.sqlite.models.expense import Expense as ExpenseModel
from koala.domain.entities.expense import Expense as ExpenseEntity, ExpenseType
from koala.infra.adapters.repositories.expenses import ExpensesRepository

@pytest.fixture
def mock_session():
    return Mock(spec=Session)

@pytest.fixture
def repository(mock_session) -> ExpensesRepository:
    return ExpensesRepository(session=mock_session)

def test_create_expense(repository: IExpensesRepository, mock_session: MagicMock):
    # Arrange
    expense = ExpenseEntity(purchased_at="2023-09-18", # type: ignore
                            name="Test Expense",
                            type=ExpenseType.FIXED,
                            amount=100.0,
                            installment_of=1,
                            installment_to=5)
    
    mock_expense_model = Mock(spec=ExpenseModel)
    mock_expense_model.id = 1

    mock_session.add.return_value = None
    mock_session.commit.return_value = None

    create_expense = Mock(repository.create_expense, wraps=repository.create_expense, return_value=mock_expense_model)

    result = create_expense(expense)
    
    assert result.id == 1