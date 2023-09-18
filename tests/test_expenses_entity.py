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

def test_installments_of_property_getter_should_be_None() -> None:
    expense = Expense(purchased_at=datetime.utcnow(),
                    name='test',
                    amount=10.3,
                    installment_of=None,
                    installment_to=None,
                    type=ExpenseType.FIXED)
    
    assert expense.installment_of is None

def test_installment_of_setter_should_only_accept_digit_parameters() -> None:
    expense = Expense(purchased_at=datetime.utcnow(),
                    name='test',
                    amount=10.3,
                    installment_of=1,
                    installment_to=5,
                    type=ExpenseType.INSTALLMENT)
    
    expense.installment_of = 3

    assert expense.installment_of == 3

def test_should_raise_exception_if_pass_non_digit_to_installment_of_setter() -> None:
    with pytest.raises(Exception, match='You should only pass digit parameters.'):
        expense = Expense(purchased_at=datetime.utcnow(),
                        name='test',
                        amount=10.3,
                        installment_of=1,
                        installment_to=5,
                        type=ExpenseType.INSTALLMENT)
        
        expense.installment_of = 'abc'

def test_should_pass_if_trying_to_set_installment_of_as_digit_str() -> None:
    expense = Expense(purchased_at=datetime.utcnow(),
                    name='test',
                    amount=10.3,
                    installment_of=1,
                    installment_to=5,
                    type=ExpenseType.INSTALLMENT)
    
    expense.installment_of = '3'

    assert expense.installment_of == 3

def test_should_raise_error_if_trying_to_set_installment_of_other_expense_type_rather_than_installment() -> None:
    with pytest.raises(Exception, match='You can only set installment to expenses of type installment.'):
        expense = Expense(purchased_at=datetime.utcnow(),
                        name='test',
                        amount=10.3,
                        installment_of=None,
                        installment_to=None,
                        type=ExpenseType.VARIABLE)
        
        expense.installment_of = 3

def test_installments_to_property_getter_should_be_None() -> None:
    expense = Expense(purchased_at=datetime.utcnow(),
                    name='test',
                    amount=10.3,
                    installment_of=None,
                    installment_to=None,
                    type=ExpenseType.FIXED)
    
    assert expense.installment_to is None

def test_installment_to_setter_should_only_accept_digit_parameters() -> None:
    expense = Expense(purchased_at=datetime.utcnow(),
                    name='test',
                    amount=10.3,
                    installment_of=1,
                    installment_to=5,
                    type=ExpenseType.INSTALLMENT)
    
    expense.installment_to = 3

    assert expense.installment_to == 3

def test_should_raise_exception_if_pass_non_digit_to_installment_to_setter() -> None:
    with pytest.raises(Exception, match='You should only pass digit parameters.'):
        expense = Expense(purchased_at=datetime.utcnow(),
                        name='test',
                        amount=10.3,
                        installment_of=1,
                        installment_to=5,
                        type=ExpenseType.INSTALLMENT)
        
        expense.installment_to = 'abc'

def test_should_pass_if_trying_to_set_installment_to_as_digit_str() -> None:
    expense = Expense(purchased_at=datetime.utcnow(),
                    name='test',
                    amount=10.3,
                    installment_of=1,
                    installment_to=5,
                    type=ExpenseType.INSTALLMENT)
    
    expense.installment_to = '3'

    assert expense.installment_to == 3

def test_should_raise_error_if_trying_to_set_installment_to_other_expense_type_rather_than_installment() -> None:
    with pytest.raises(Exception, match='You can only set installment to expenses of type installment.'):
        expense = Expense(purchased_at=datetime.utcnow(),
                        name='test',
                        amount=10.3,
                        installment_of=None,
                        installment_to=None,
                        type=ExpenseType.VARIABLE)
        
        expense.installment_to = 3

