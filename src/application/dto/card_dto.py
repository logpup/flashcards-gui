from uuid import UUID

from pydantic import BaseModel, Field
from typing import Optional

class CardDTO(BaseModel):
    """Shared properties for Card DTOs."""
    front: str = Field(..., min_length=1, description="Font of the card")
    back: str = Field(..., min_length=1, description="Back of the card")

class CardCreateDTO(CardDTO):
    """Used for creating a new card (no ID yet)."""
    deck_id: Optional[UUID] = Field(None, description="Associated deck ID")

class CardReadDTO(CardDTO):
    """Used when reading card data from DB."""
    id: UUID = Field(..., description="Unique identifier for the card")
    deck_id: Optional[UUID] = None

    class Config:
        orm_mode = True # allows conversion from SQLAlchemy ORM to Pydantic
