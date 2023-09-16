import sys

sys.path.insert(0, '../')

import pytest
from datetime import datetime
from koala.domain.entities.expense import Expense, ExpenseType

def test_installment_of_cannot_be_greater_than_installment_to() -> None:
    with pytest.raises(Exception, match='You cant create an expense with installment of greater than installment to.'):
        Expense(purchased_at=datetime.utcnow(),
                name='test',
                amount=10.3,
                installment_of=3,
                installment_to=1,
                type=ExpenseType.INSTALLMENT)

def test_installment_of_and_to_must_be_defined() -> None:
    with pytest.raises(Exception, match='You must define installment_of and installment_to because this expense was labeled as installment.'):
        Expense(purchased_at=datetime.utcnow(),
                name='test',
                amount=10.3,
                installment_of=None,
                installment_to=None,
                type=ExpenseType.INSTALLMENT)
        
def test_create_expense_successfully() -> None:
    expense = Expense(purchased_at=datetime.utcnow(),
                    name='test',
                    amount=10.3,
                    installment_of=3,
                    installment_to=3,
                    type=ExpenseType.INSTALLMENT)
    
    assert expense.installment_of == 3
    assert expense.installment_of == 3
    assert expense.type == ExpenseType.INSTALLMENT