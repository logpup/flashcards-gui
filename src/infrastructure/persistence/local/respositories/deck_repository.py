# Local application imports
from src.infrastructure.persistence.local.connection import get_session
from src.infrastructure.persistence.local.schemas.deck_schema import DeckORM
from src.infrastructure.persistence.local.schemas.card_schema import CardORM
from src.domain.models.deck import Deck
from src.domain.models.card import Card


class SqlAlchemyDeckRepository:
    """Handles CRUD operations for Deck entities using SQLAlchemy."""

    def add(self, deck: Deck) -> Deck:
        """Adds a new Deck to the database with its cards."""
        with get_session() as session:
            orm_deck = DeckORM(
                id=str(deck.id),
                name=deck.name,
            )
            
            # Add cards if present
            for card in deck.cards:
                orm_card = CardORM(
                    id=str(card.id),
                    front=card.front,
                    back=card.back,
                    deck_id=str(deck.id),
                )
                orm_deck.cards.append(orm_card)
            
            session.add(orm_deck)
            session.flush()
        return deck
    
    def get_by_id(self, deck_id: str) -> Deck | None:
        """Retrieves a deck by its ID, including its cards."""
        with get_session() as session:
            orm_deck = session.query(DeckORM).filter_by(id=str(deck_id)).first()
            if orm_deck:
                cards = [
                    Card(id=c.id, front=c.front, back=c.back)
                    for c in orm_deck.cards
                ]
                return Deck(
                    id=orm_deck.id,
                    name=orm_deck.name,
                    cards=cards,
                )
            return None
    
    def list_all(self) -> list[Deck]:
        """Lists all decks in the database."""
        with get_session() as session:
            orm_decks = session.query(DeckORM).all()
            decks = []
            for d in orm_decks:
                cards = [
                    Card(id=c.id, front=c.front, back=c.back)
                    for c in d.cards
                ]
                decks.append(Deck(id=d.id, name=d.name, cards=cards))
            return decks
    
    def update(self, deck: Deck) -> Deck | None:
        """Updates an existing deck."""
        with get_session() as session:
            orm_deck = session.query(DeckORM).filter_by(id=str(deck.id)).first()
            if orm_deck:
                orm_deck.name = deck.name
                session.flush()
                return deck
            return None
    
    def delete(self, deck_id: str) -> bool:
        """Deletes a deck by its ID. Returns True if deleted, False if not found."""
        with get_session() as session:
            orm_deck = session.query(DeckORM).filter_by(id=str(deck_id)).first()
            if orm_deck:
                session.delete(orm_deck)
                session.flush()
                return True
            return False
    
    def add_card_to_deck(self, deck_id: str, card: Card) -> bool:
        """Adds a card to an existing deck."""
        with get_session() as session:
            orm_deck = session.query(DeckORM).filter_by(id=str(deck_id)).first()
            if orm_deck:
                orm_card = CardORM(
                    id=str(card.id),
                    front=card.front,
                    back=card.back,
                    deck_id=str(deck_id),
                )
                session.add(orm_card)
                session.flush()
                return True
            return False