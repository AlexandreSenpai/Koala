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

    def __init__(self,
                 purchased_at: datetime,
                 name: str,
                 type: ExpenseType,
                 amount: float,
                 installment_of: Union[int, None] = None,
                 installment_to: Union[int, None] = None,
                 id: Union[int, str, None] = None, 
                 created_at: Union[datetime, None] = None, 
                 updated_at: Union[datetime, None] = None) -> None:
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
        return self._installment_of

    @property
    def installment_to(self) -> Union[int, None]:
        return self._installment_to

    @installment_of.setter
    def installment_of(self, installment: int):
        self._installment_of = int(installment)
    
    @installment_to.setter
    def installment_to(self, installment: int):
        self._installment_to = int(installment)
