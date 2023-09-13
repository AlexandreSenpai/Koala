from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Union
from koala.domain.entities.base import Entity

class ExpenseType(Enum):
    FIXED = 'fixed'
    INSTALLMENT = 'installment'
    VARIABLE = 'variable'

@dataclass
class Expense(Entity):
    purchased_at: datetime
    name: str
    type: ExpenseType
    amount: float
    installment_of: int = None
    installment_to: int = None

    def __init__(self,
                 purchased_at: datetime,
                 name: str,
                 type: ExpenseType,
                 amount: float,
                 installment_of: int = None,
                 installment_to: int = None,
                 id: Union[int, str] = None, 
                 created_at: datetime = None, 
                 updated_at: datetime = None) -> None:
        super().__init__(id=id, 
                         created_at=created_at, 
                         updated_at=updated_at)
        self.purchased_at = purchased_at
        self.name = name
        self.type = type
        self.amount = amount
        self._installment_of = int(installment_of) if installment_of is not None else None
        self._installment_to = int(installment_to) if installment_to is not None else None
    
    @property
    def installment_of(self) -> Union[int, None]:
        return self._installment_of \
            if self._installment_of is not None \
            and self._installment_to > 0 \
            and self._installment_of <= self._installment_to \
            and self._installment_of != "" \
            else None

    @property
    def installment_to(self) -> Union[int, None]:
        return self._installment_to \
            if self._installment_to is not None \
            and self._installment_to >= self._installment_of \
            and self._installment_to != "" \
            else None

    @installment_of.setter
    def installment_of(self, installment: int):
        self._installment_of = int(installment)
    
    @installment_to.setter
    def installment_to(self, installment: int):
        self._installment_to = int(installment)