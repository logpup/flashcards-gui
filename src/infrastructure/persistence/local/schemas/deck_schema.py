# Standard library imports
from uuid import uuid4

# Third-party imports
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

# Local application imports
from src.infrastructure.persistence.local.connection import Base


class DeckORM(Base):
    """ORM schema for the 'decks' table"""
    __tablename__ = "decks"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    name = Column(String, nullable=False)

    # Relationship to cards
    cards = relationship("CardORM", back_populates="deck", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<DeckORM(id={self.id}, name={self.name!r})>"