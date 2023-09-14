from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Any, TypeVar, Union

T = TypeVar('T')

@dataclass
class Entity:
    id: Union[int, str]
    created_at: datetime
    updated_at: datetime

    def __init__(self, 
                 id: Union[int, str, None] = None,
                 created_at: Union[datetime, None] = None,
                 updated_at: Union[datetime, None] = None) -> None:
        self.id = id if id is not None else 0
        self.created_at = created_at if created_at is not None else datetime.utcnow()
        self.updated_at = updated_at if updated_at is not None else datetime.utcnow()

    def to_dict(self) -> Any:
        return asdict(self)