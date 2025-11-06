"""
ORM Schema definitions for SQLAlchemy

Import all ORM models here so they're registered with SQLAlchemy's Base.metadata
"""

from src.infrastructure.persistence.local.schemas.card_schema import CardORM
from src.infrastructure.persistence.local.schemas.deck_schema import DeckORM

__all__ = ['CardORM', 'DeckORM']