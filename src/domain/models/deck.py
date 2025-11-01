# Standard library imports
from dataclasses import dataclass, field
from typing import List, Optional
from uuid import UUID, uuid4

# Local application imports
from domain.models.card import Card


@dataclass
class Deck:
    name: str
    id: UUID = field(default_factory=uuid4)
    cards: List['Card'] = field(default_factory=list)

    @classmethod
    def create(cls, name: str, cards: Optional[List['Card']] = None):
        if cards is None:
            cards = []
        return cls(name=name, cards=cards)

    def add(self, cards: Optional[List['Card']] = None):
        self.cards.extend(cards)

def test_add_cards_to_deck():
    # Create deck
    deck = Deck.create(name="Test Deck")
    assert len(deck.cards) == 0

    # Create cards
    card1 = Card.create(front="foo", back="bar")
    card2 = Card.create(front="hello", back="world")

    # Add cards to deck
    deck.add(cards=[card1, card2])
    
    assert len(deck.cards) == 2
    assert deck.cards[0] == card1
    assert deck.cards[1] == card2
    print("Test passed!")

# Run test
test_add_cards_to_deck()