from datetime import datetime

from sqlalchemy import Column, DateTime, Enum, Float, Integer, String

from koala.infra.adapters.database.sqlite.models.base import Base

class Expense(Base):
    """SQLAlchemy model for the Expense entity.

    This class maps the Expense entity to a SQL table and defines its structure.

    Attributes:
        __tablename__: A string representing the name of the table in the database.
        id: An integer column serving as the unique identifier for each expense.
        created_at: A DateTime column representing when the expense was created.
        updated_at: A DateTime column representing when the expense was last updated.
        purchased_at: A DateTime column representing the date of purchase.
        name: A String column representing the name of the expense.
        type: An Enum column representing the type of expense.
        installment_of: An Integer column representing the current installment number.
        installment_to: An Integer column representing the total number of installments.
        amount: A Float column representing the amount of the expense.
    """
    __tablename__ = 'expenses'

    id = Column(Integer,
                autoincrement=True, 
                unique=True, 
                primary_key=True,
                nullable=False)
    created_at = Column(DateTime, 
                        default=datetime.utcnow)
    updated_at = Column(DateTime, 
                        default=datetime.utcnow, 
                        onupdate=datetime.utcnow)
    purchased_at = Column(DateTime, 
                          nullable=False)
    name = Column(String, 
                  nullable=False)
    type = Column(Enum('fixed', 'variable', 'installment'),
                  nullable=False)
    installment_of = Column(Integer,
                            nullable=True,
                            default=None)
    installment_to = Column(Integer,
                            nullable=True,
                            default=None)
    amount = Column(Float(2), 
                    nullable=False, 
                    default=0.0)
