from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Generic, Optional, TypeVar, Union, cast

T = TypeVar('T')

@dataclass
class Entity(Generic[T]):
    """Base class for entities in the domain model.

    This class provides common attributes and methods for all entities.

    Attributes:
        id: A Union of int and str representing the entity's ID.
        created_at: A datetime object representing when the entity was created.
        updated_at: A datetime object representing when the entity was last updated.
    """

    id: Union[int, str]
    __created_at: datetime
    updated_at: datetime

    def __init__(self, 
                 id: Optional[Union[int, str]] = None,
                 created_at: Optional[datetime] = None,
                 updated_at: Optional[datetime] = None) -> None:
        """Initializes an Entity with given or default values.

        Args:
            id: A Union of int, str, and None representing the entity's ID. Defaults to 0.
            created_at: A Union of datetime and None representing when the entity was created. Defaults to current UTC time.
            updated_at: A Union of datetime and None representing when the entity was last updated. Defaults to current UTC time.
        """

        if not id is None and not isinstance(id, str) and not isinstance(id, int):
            raise Exception('Id must be an str or int value.')

        self.id = id if id is not None else 0
        self.__created_at = created_at if created_at is not None else datetime.utcnow()
        self.updated_at = updated_at if updated_at is not None else datetime.utcnow()

    @property
    def created_at(self) -> datetime:
        """Created at must be immutable.

        Returns:
            created_at: datetime value representing the entity creation date.
        """
        return self.__created_at
    
    def to_dict(self) -> T:
        """Converts the entity to a dictionary.

        Returns:
            A dictionary representation of the entity.
        """
        keys_to_omit = ['_Entity__created_at']
        object_omitted = {key: val for key, val in asdict(self).items() if key not in keys_to_omit}
        return cast(T, {**object_omitted, 
                        'created_at': self.created_at})