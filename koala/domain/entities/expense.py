from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional, Union, cast
from koala.domain.entities.base import Entity

class ExpenseType(Enum):
    """Enum to represent the type of an expense.

    Attributes:
        FIXED: A fixed expense.
        INSTALLMENT: An expense paid in installments.
        VARIABLE: A variable expense.
    """
    FIXED = 'fixed'
    INSTALLMENT = 'installment'
    VARIABLE = 'variable'

@dataclass
class Expense(Entity):
    """Class to represent an Expense entity.

    This class inherits from the Entity base class and adds additional attributes
    specific to an expense.

    Attributes:
        purchased_at: A datetime object representing the date of purchase.
        name: A string representing the name of the expense.
        type: An ExpenseType enum representing the type of expense.
        amount: A float representing the amount of the expense.
    """
    purchased_at: datetime
    name: str
    type: ExpenseType
    amount: float

    def __init__(self,
                 purchased_at: datetime,
                 name: str,
                 type: ExpenseType,
                 amount: float,
                 installment_of: Optional[int] = None,
                 installment_to: Optional[int] = None,
                 id: Optional[Union[int, str]] = None, 
                 created_at: Optional[datetime] = None, 
                 updated_at: Optional[datetime] = None) -> None:
        """Initializes an Expense entity with given or default values.

        Args:
            purchased_at: A datetime object representing the date of purchase.
            name: A string representing the name of the expense.
            type: An ExpenseType enum representing the type of expense.
            amount: A float representing the amount of the expense.
            installment_of: An optional integer representing the current installment number.
            installment_to: An optional integer representing the total number of installments.
            id: An optional Union of int, str, and None representing the entity's ID.
            created_at: An optional Union of datetime and None representing when the entity was created.
            updated_at: An optional Union of datetime and None representing when the entity was last updated.
        """
        super().__init__(id=id, 
                         created_at=created_at, 
                         updated_at=updated_at)
        self.purchased_at = purchased_at
        self.name = name
        self.type = type
        self.amount = amount

        self._installment_of = int(installment_of) if installment_of is not None else None
        self._installment_to = int(installment_to) if installment_to is not None else None

        if type == ExpenseType.INSTALLMENT: self.validate_installments(installment_of=cast(int, self._installment_of),
                                                                       installment_to=cast(int, self._installment_to))
    
    def validate_installments(self,
                              installment_of: Optional[int] = None, 
                              installment_to: Optional[int] = None) -> None:
        if installment_of is None or installment_to is None:
            raise Exception('You must define installment_of and installment_to because this expense was labeled as installment.')
        if installment_of > installment_to:
            raise Exception('You cant create an expense with installment of greater than installment to.')

    @property
    def installment_of(self) -> Optional[int]:
        """Property to get the current installment number.

        Returns:
            An integer or None representing the current installment number.
        """
        return self._installment_of

    @property
    def installment_to(self) -> Optional[int]:
        """Property to get the total number of installments.

        Returns:
            An integer or None representing the total number of installments.
        """
        return self._installment_to

    @installment_of.setter
    def installment_of(self, 
                       installment: int):
        """Setter for the current installment number.

        Args:
            installment: An integer representing the current installment number.
        """
        self._installment_of = int(installment)
    
    @installment_to.setter
    def installment_to(self, 
                       installment: int):
        """Setter for the total number of installments.

        Args:
            installment: An integer representing the total number of installments.
        """
        self._installment_to = int(installment)
