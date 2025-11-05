# Local application imports

from domain.models.card import Card
from domain.models.deck import Deck


def test_add_cards_to_deck():
    """
    Tests that adding multiple Card objects to a Deck updates the card count
    and preserves insertion order.
    """
    # Arrange
    deck = Deck.create(name="Test Deck")
    assert len(deck.cards) == 0

    card1 = Card.create(front="foo", back="bar")
    card2 = Card.create(front="hello", back="world")

    # Act
    deck.add(cards=[card1, card2])
    
    # Assert
    assert len(deck.cards) == 2
    assert deck.cards == [card1, card2]