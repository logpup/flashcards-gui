# Standard library imports
from dataclasses import dataclass
from uuid import UUID, uuid4


@dataclass
class Card:
    id: UUID
    front: str
    back: str

    @classmethod
    def create(cls, front: str, back: str):
        return cls(id=uuid4(), front=front, back=back)