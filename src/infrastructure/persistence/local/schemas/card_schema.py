# Standard library imports
from uuid import UUID, uuid4

# Third-party imports
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

# Local application imports
from src.infrastructure.persistence.local.connection import Base


class CardORM(Base):
    """
    ORM schema for the 'cards' table.
    Defines how Card objects are stored in the database.
    """
    __tablename__ = "cards"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    front = Column(String, nullable=False)
    back = Column(String, nullable=False)
    deck_id = Column(String, ForeignKey("decks.id"), nullable=True)

    deck = relationship("DeckORM", back_populates="cards")

    def __repr__(self):
        return f"<CardORM(id={self.id}, front={self.front!r}, back={self.back!r})>"