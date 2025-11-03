# Standard library imports

from uuid import UUID, uuid4


# Third-party imports

from pydantic import BaseModel, Field


class Card(BaseModel):
    """Domain entity representing a flashcard."""
    id: UUID = Field(default_factory=uuid4)
    front: str = Field(..., min_length=1, description="Front of the card")
    back: str = Field(..., min_length=1, description="Back of the card")

    @classmethod
    def create(cls, front: str, back: str):
        """Factory method to create a new Card instance."""
        return cls(id=uuid4(), front=front, back=back)