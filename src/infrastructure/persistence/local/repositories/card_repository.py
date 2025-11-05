# Local application imports
from src.infrastructure.persistence.local.connection import get_session
from src.infrastructure.persistence.local.schemas.card_schema import CardORM
from src.domain.models.card import Card


class SqlAlchemyCardRepository:
    """Handles CRUD operations for Card entities using SQLAlchemy."""

    def add(self, card: Card) -> Card:
        """Adds a new card to the database."""
        with get_session() as session:
            orm_card = CardORM(
                id=str(card.id),
                front=card.front,
                back=card.back,
                deck_id=str(card.id) if hasattr(card, "deck_id") else None,
            )
            session.add(orm_card)
            session.flush()
        return card
    
    def get_by_id(self, card_id: str) -> Card | None:
        """Retrieves a card by its ID."""
        with get_session() as session:
            orm_card = session.query(CardORM).filter_by(id=str(card_id)).first()
            if orm_card:
                return Card(
                    id=orm_card.id,
                    front=orm_card.front,
                    back=orm_card.back,
                )
            return None
    
    def list_all(self) -> list[Card]:
        """Lists all cards in the database."""
        with get_session() as session:
            orm_cards = session.query(CardORM).all()
            return [Card(id=c.id, front=c.front, back=c.back) for c in orm_cards]
    
    def update(self, card: Card) -> Card | None:
        """Updates an existing card."""
        with get_session() as session:
            orm_card = session.query(CardORM).filter_by(id=str(card.id)).first()
            if orm_card:
                orm_card.front = card.front
                orm_card.back = card.back
                session.flush()
                return card
            return None
        
    def delete(self, card_id: str) -> bool:
        """Deletes a card by its ID."""
        with get_session() as session:
            orm_card = session.query(CardORM).filter_by(id=str(card_id)).first()
            if orm_card:
                session.delete(orm_card)
                session.commit()
                return True
            return False
