# Standard library imports
import pytest
from uuid import uuid4

# Third-party imports
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Local application imports
from src.domain.models.card import Card
from src.infrastructure.persistence.local.connection import Base
from src.infrastructure.persistence.local.schemas.card_schema import CardORM
from src.infrastructure.persistence.local.repositories.card_repository import SqlAlchemyCardRepository


@pytest.fixture(scope="function")
def test_engine():
    """Create an in-memory SQLite database for testing."""
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def test_session(test_engine, monkeypatch):
    """Create a test session and monkey-patch the SessionLocal."""
    TestSessionLocal = sessionmaker(bind=test_engine, autocommit=False, autoflush=False)
    
    # Monkey-patch the SessionLocal in connection module
    import src.infrastructure.persistence.local.connection as conn
    monkeypatch.setattr(conn, "SessionLocal", TestSessionLocal)
    
    yield TestSessionLocal
    

@pytest.fixture
def repository(test_session):
    """Create a repository instance for testing."""
    return SqlAlchemyCardRepository()


@pytest.fixture
def sample_card():
    """Create a sample card for testing."""
    return Card.create(front="What is Python?", back="A programming language")


class TestCardRepository:
    """Test suite for SqlAlchemyCardRepository."""
    
    def test_add_card(self, repository, sample_card):
        """Test adding a new card to the database."""
        result = repository.add(sample_card)
        
        assert result is not None
        assert result.id == sample_card.id
        assert result.front == sample_card.front
        assert result.back == sample_card.back
    
    def test_get_card_by_id(self, repository, sample_card):
        """Test retrieving a card by its ID."""
        repository.add(sample_card)
        
        retrieved_card = repository.get_by_id(str(sample_card.id))
        
        assert retrieved_card is not None
        assert str(retrieved_card.id) == str(sample_card.id)
        assert retrieved_card.front == sample_card.front
        assert retrieved_card.back == sample_card.back
    
    def test_get_card_by_id_not_found(self, repository):
        """Test retrieving a non-existent card returns None."""
        non_existent_id = str(uuid4())
        result = repository.get_by_id(non_existent_id)
        
        assert result is None
    
    def test_list_all_cards_empty(self, repository):
        """Test listing cards when database is empty."""
        cards = repository.list_all()
        
        assert cards == []
    
    def test_list_all_cards(self, repository):
        """Test listing all cards in the database."""
        card1 = Card.create(front="Question 1", back="Answer 1")
        card2 = Card.create(front="Question 2", back="Answer 2")
        card3 = Card.create(front="Question 3", back="Answer 3")
        
        repository.add(card1)
        repository.add(card2)
        repository.add(card3)
        
        cards = repository.list_all()
        
        assert len(cards) == 3
        assert any(str(c.id) == str(card1.id) for c in cards)
        assert any(str(c.id) == str(card2.id) for c in cards)
        assert any(str(c.id) == str(card3.id) for c in cards)
    
    def test_update_card(self, repository, sample_card):
        """Test updating an existing card."""
        repository.add(sample_card)
        
        # Update the card
        sample_card.front = "Updated question"
        sample_card.back = "Updated answer"
        
        updated_card = repository.update(sample_card)
        
        assert updated_card is not None
        assert updated_card.front == "Updated question"
        assert updated_card.back == "Updated answer"
        
        # Verify in database
        retrieved_card = repository.get_by_id(str(sample_card.id))
        assert retrieved_card.front == "Updated question"
        assert retrieved_card.back == "Updated answer"
    
    def test_update_card_not_found(self, repository):
        """Test updating a non-existent card returns None."""
        card = Card.create(front="Test", back="Test")
        result = repository.update(card)
        
        assert result is None
    
    def test_delete_card(self, repository, sample_card):
        """Test deleting a card from the database."""
        repository.add(sample_card)
        
        # Verify card exists
        assert repository.get_by_id(str(sample_card.id)) is not None
        
        # Delete the card
        result = repository.delete(str(sample_card.id))
        
        assert result is True
        assert repository.get_by_id(str(sample_card.id)) is None
    
    def test_delete_card_not_found(self, repository):
        """Test deleting a non-existent card returns False."""
        non_existent_id = str(uuid4())
        result = repository.delete(non_existent_id)
        
        assert result is False
    
    def test_add_multiple_cards(self, repository):
        """Test adding multiple cards in sequence."""
        cards = [
            Card.create(front=f"Question {i}", back=f"Answer {i}")
            for i in range(5)
        ]
        
        for card in cards:
            repository.add(card)
        
        all_cards = repository.list_all()
        assert len(all_cards) == 5
    
    def test_card_persistence(self, repository, sample_card):
        """Test that cards persist correctly."""
        repository.add(sample_card)
        
        # Retrieve multiple times to ensure persistence
        card1 = repository.get_by_id(str(sample_card.id))
        card2 = repository.get_by_id(str(sample_card.id))
        
        assert str(card1.id) == str(card2.id)
        assert card1.front == card2.front
        assert card1.back == card2.back