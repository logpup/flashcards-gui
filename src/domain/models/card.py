# Standard library imports

from uuid import UUID, uuid4

# Third-party imports
from pydantic import BaseModel, Field


class Card(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    front: str = Field(..., min_length=1, description="Front of the card")
    back: str = Field(..., min_length=1, description="Back of the card")

    @classmethod
    def create(cls, front: str, back: str):
        return cls(id=uuid4(), front=front, back=back)