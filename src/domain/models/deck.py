# Standard library imports
from typing import List, Optional
from uuid import UUID, uuid4

# Third-party imports
from pydantic import BaseModel, Field

# Local application imports
from src.domain.models.card import Card


class Deck(BaseModel):
    name: str
    id: UUID = Field(default_factory=uuid4)
    cards: List['Card'] = Field(default_factory=list)

    @classmethod
    def create(cls, name: str, cards: Optional[List['Card']] = None):
        if cards is None:
            cards = []
        return cls(name=name, cards=cards)

    def add(self, cards: Optional[List['Card']] = None):
        self.cards.extend(cards)
