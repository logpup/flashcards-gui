# Standard library imports
import pytest
from uuid import uuid4

# Third-party imports
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Local application imports
from src.domain.models.card import Card
from src.domain.models.deck import Deck
from src.infrastructure.persistence.local.connection import Base
from src.infrastructure.persistence.local.repositories.deck_repository import SqlAlchemyDeckRepository


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
    return SqlAlchemyDeckRepository()


@pytest.fixture
def sample_cards():
    """Create sample cards for testing."""
    return [
        Card.create(front="Question 1", back="Answer 1"),
        Card.create(front="Question 2", back="Answer 2"),
        Card.create(front="Question 3", back="Answer 3"),
    ]


@pytest.fixture
def sample_deck(sample_cards):
    # 1. Convert the list of Card model instances to a list of dictionaries
    card_data = [card.model_dump() for card in sample_cards]
    
    # 2. Pass the list of dictionaries to the constructor
    return Deck.create(name="Python Basics", cards=card_data)


@pytest.fixture
def empty_deck():
    """Create an empty deck for testing."""
    return Deck.create(name="Empty Deck")


class TestDeckRepository:
    """Test suite for SqlAlchemyDeckRepository."""
    
    def test_add_deck_with_cards(self, repository, sample_deck):
        """Test adding a new deck with cards to the database."""
        result = repository.add(sample_deck)
        
        assert result is not None
        assert result.id == sample_deck.id
        assert result.name == sample_deck.name
        assert len(result.cards) == 3
    
    def test_add_empty_deck(self, repository, empty_deck):
        """Test adding an empty deck to the database."""
        result = repository.add(empty_deck)
        
        assert result is not None
        assert result.id == empty_deck.id
        assert result.name == empty_deck.name
        assert len(result.cards) == 0
    
    def test_get_deck_by_id(self, repository, sample_deck):
        """Test retrieving a deck by its ID."""
        repository.add(sample_deck)
        
        retrieved_deck = repository.get_by_id(str(sample_deck.id))
        
        assert retrieved_deck is not None
        assert str(retrieved_deck.id) == str(sample_deck.id)
        assert retrieved_deck.name == sample_deck.name
        assert len(retrieved_deck.cards) == 3
    
    def test_get_deck_by_id_not_found(self, repository):
        """Test retrieving a non-existent deck returns None."""
        non_existent_id = str(uuid4())
        result = repository.get_by_id(non_existent_id)
        
        assert result is None
    
    def test_get_deck_with_cards(self, repository, sample_deck):
        """Test that retrieved deck includes all its cards."""
        repository.add(sample_deck)
        
        retrieved_deck = repository.get_by_id(str(sample_deck.id))
        
        assert len(retrieved_deck.cards) == len(sample_deck.cards)
        
        # Check that cards match
        original_ids = {str(c.id) for c in sample_deck.cards}
        retrieved_ids = {str(c.id) for c in retrieved_deck.cards}
        assert original_ids == retrieved_ids
    
    def test_list_all_decks_empty(self, repository):
        """Test listing decks when database is empty."""
        decks = repository.list_all()
        
        assert decks == []
    
    def test_list_all_decks(self, repository):
        """Test listing all decks in the database."""
        deck1 = Deck.create(name="Deck 1")
        deck2 = Deck.create(name="Deck 2")
        deck3 = Deck.create(name="Deck 3")
        
        repository.add(deck1)
        repository.add(deck2)
        repository.add(deck3)
        
        decks = repository.list_all()
        
        assert len(decks) == 3
        deck_names = {d.name for d in decks}
        assert deck_names == {"Deck 1", "Deck 2", "Deck 3"}
    
    def test_list_all_decks_with_cards(self, repository, sample_deck):
        """Test that listing decks includes their cards."""
        repository.add(sample_deck)
        
        decks = repository.list_all()
        
        assert len(decks) == 1
        assert len(decks[0].cards) == 3
    
    def test_update_deck(self, repository, sample_deck):
        """Test updating an existing deck."""
        repository.add(sample_deck)
        
        # Update the deck name
        sample_deck.name = "Updated Deck Name"
        
        updated_deck = repository.update(sample_deck)
        
        assert updated_deck is not None
        assert updated_deck.name == "Updated Deck Name"
        
        # Verify in database
        retrieved_deck = repository.get_by_id(str(sample_deck.id))
        assert retrieved_deck.name == "Updated Deck Name"
    
    def test_update_deck_not_found(self, repository):
        """Test updating a non-existent deck returns None."""
        deck = Deck.create(name="Test Deck")
        result = repository.update(deck)
        
        assert result is None
    
    def test_delete_deck(self, repository, sample_deck):
        """Test deleting a deck from the database."""
        repository.add(sample_deck)
        
        # Verify deck exists
        assert repository.get_by_id(str(sample_deck.id)) is not None
        
        # Delete the deck
        result = repository.delete(str(sample_deck.id))
        
        assert result is True
        assert repository.get_by_id(str(sample_deck.id)) is None
    
    def test_delete_deck_not_found(self, repository):
        """Test deleting a non-existent deck returns False."""
        non_existent_id = str(uuid4())
        result = repository.delete(non_existent_id)
        
        assert result is False
    
    def test_delete_deck_cascades_to_cards(self, repository, sample_deck):
        """Test that deleting a deck also deletes its cards."""
        repository.add(sample_deck)
        
        # Delete the deck
        repository.delete(str(sample_deck.id))
        
        # Verify deck and cards are gone
        deck = repository.get_by_id(str(sample_deck.id))
        assert deck is None
    
    def test_add_card_to_deck(self, repository, empty_deck):
        """Test adding a card to an existing deck."""
        repository.add(empty_deck)
        
        new_card = Card.create(front="New Question", back="New Answer")
        result = repository.add_card_to_deck(str(empty_deck.id), new_card)
        
        assert result is True
        
        # Verify card was added
        retrieved_deck = repository.get_by_id(str(empty_deck.id))
        assert len(retrieved_deck.cards) == 1
        assert retrieved_deck.cards[0].front == "New Question"
    
    def test_add_card_to_nonexistent_deck(self, repository):
        """Test adding a card to a non-existent deck returns False."""
        non_existent_id = str(uuid4())
        new_card = Card.create(front="Test", back="Test")
        
        result = repository.add_card_to_deck(non_existent_id, new_card)
        
        assert result is False
    
    def test_add_multiple_cards_to_deck(self, repository, empty_deck):
        """Test adding multiple cards to a deck."""
        repository.add(empty_deck)
        
        cards = [
            Card.create(front=f"Question {i}", back=f"Answer {i}")
            for i in range(5)
        ]
        
        for card in cards:
            repository.add_card_to_deck(str(empty_deck.id), card)
        
        retrieved_deck = repository.get_by_id(str(empty_deck.id))
        assert len(retrieved_deck.cards) == 5
    
    def test_deck_persistence(self, repository, sample_deck):
        """Test that decks persist correctly."""
        repository.add(sample_deck)
        
        # Retrieve multiple times to ensure persistence
        deck1 = repository.get_by_id(str(sample_deck.id))
        deck2 = repository.get_by_id(str(sample_deck.id))
        
        assert str(deck1.id) == str(deck2.id)
        assert deck1.name == deck2.name
        assert len(deck1.cards) == len(deck2.cards)
    
    def test_multiple_decks_with_cards(self, repository, sample_cards):
        """Test managing multiple decks with cards."""
        deck1 = Deck.create(name="Deck 1", cards=sample_cards[:2])
        deck2 = Deck.create(name="Deck 2", cards=[sample_cards[2]])
        
        repository.add(deck1)
        repository.add(deck2)
        
        all_decks = repository.list_all()
        assert len(all_decks) == 2
        
        # Verify card counts
        deck_card_counts = {d.name: len(d.cards) for d in all_decks}
        assert deck_card_counts["Deck 1"] == 2
        assert deck_card_counts["Deck 2"] == 1