from datetime import datetime

from sqlalchemy import Column, DateTime, Enum, Float, Integer, String

from koala.infra.adapters.database.sqlite.models.base import Base

class Expense(Base):
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
