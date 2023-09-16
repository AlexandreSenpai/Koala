from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Generic, Optional, TypeVar, Union

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
    created_at: datetime
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

        self.id = id if id is not None else 0
        self.created_at = created_at if created_at is not None else datetime.utcnow()
        self.updated_at = updated_at if updated_at is not None else datetime.utcnow()

    def to_dict(self) -> T:
        """Converts the entity to a dictionary.

        Returns:
            A dictionary representation of the entity.
        """
        return asdict(self) # type: ignore