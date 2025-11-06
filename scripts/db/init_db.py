#!/usr/bin/env python3
"""
Initialize database with schema and optional sample data
"""
import sys
import os
import argparse
from pathlib import Path

# Add project root to Python path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Set environment before importing models
def setup_environment(env: str):
    os.environ['ENVIRONMENT'] = env

def create_database(env: str = 'development', force: bool = False, with_sample_data: bool = True):
    """Create database with schema and optional sample data"""
    
    # Set environment
    setup_environment(env)
    
    # Import after environment is set
    from src.infrastructure.persistence.local.connection import (
        init_db, drop_db, get_db_info, DB_PATH
    )
    
    # Get database info
    db_info = get_db_info()
    
    print(f"\n{'='*60}")
    print(f"Initializing {env.upper()} Database")
    print(f"{'='*60}")
    print(f"Path: {db_info['database_path']}")
    print(f"Exists: {db_info['database_exists']}")
    
    # Check if database exists
    if db_info['database_exists'] and not force:
        response = input(f"\nDatabase already exists. Overwrite? (yes/no): ")
        if response.lower() != 'yes':
            print("❌ Initialization cancelled.")
            return
    
    # Drop existing database if force or user confirmed
    if db_info['database_exists']:
        print("\n🗑️  Dropping existing tables...")
        drop_db()
        print("✓ Tables dropped")
    
    # Import ORM models before creating database
    # This ensures SQLAlchemy knows about all tables
    from src.infrastructure.persistence.local.schemas.card_schema import CardORM
    from src.infrastructure.persistence.local.schemas.deck_schema import DeckORM
    
    # Create new database
    print("\n🔨 Creating database schema...")
    init_db()
    
    # Add sample data if requested
    if with_sample_data and env in ['development', 'test']:
        print(f"\n📦 Adding sample data for {env} environment...")
        add_sample_data(env)
    
    print(f"\n{'='*60}")
    print(f"✅ {env.upper()} database ready!")
    print(f"{'='*60}")
    print(f"Location: {db_info['absolute_path']}")
    print(f"\nTo view in DBeaver:")
    print(f"  1. New Connection → SQLite")
    print(f"  2. Browse to: {db_info['absolute_path']}")
    print(f"  3. Test Connection → Finish")
    print()

def add_sample_data(env: str):
    """Add sample data appropriate for the environment"""
    from src.domain.models.card import Card
    from src.domain.models.deck import Deck
    from src.infrastructure.persistence.local.repositories.deck_repository import SqlAlchemyDeckRepository
    from src.infrastructure.persistence.local.repositories.card_repository import SqlAlchemyCardRepository
    
    deck_repo = SqlAlchemyDeckRepository()
    card_repo = SqlAlchemyCardRepository()
    
    if env == 'test':
        # Minimal data for automated tests
        print("  Adding minimal test fixtures...")
        
        deck = Deck.create(name="Test Deck")
        card1 = Card.create(front="Test Question 1", back="Test Answer 1")
        deck.add([card1])
        
        deck_repo.add(deck)
        print(f"    ✓ Created 1 deck with 1 card")
    
    elif env == 'development':
        # Rich data for manual development testing
        print("  Adding diverse development data...")
        
        # Spanish Deck
        spanish_cards = [
            Card.create(front="Hello", back="Hola"),
            Card.create(front="Goodbye", back="Adiós"),
            Card.create(front="Thank you", back="Gracias"),
            Card.create(front="Please", back="Por favor"),
            Card.create(front="Water", back="Agua"),
        ]
        spanish_deck = Deck.create(name="Spanish Vocabulary", cards=spanish_cards)
        deck_repo.add(spanish_deck)
        
        # Python Programming Deck
        python_cards = [
            Card.create(
                front="What is a list comprehension in Python?",
                back="A concise way to create lists: [x for x in iterable]"
            ),
            Card.create(
                front="What does 'self' represent in Python classes?",
                back="The instance of the class"
            ),
            Card.create(
                front="What is the difference between '==' and 'is'?",
                back="'==' compares values, 'is' compares object identity"
            ),
            Card.create(
                front="What is a decorator in Python?",
                back="A function that modifies the behavior of another function"
            ),
        ]
        python_deck = Deck.create(name="Python Programming", cards=python_cards)
        deck_repo.add(python_deck)
        
        # Math Deck
        math_cards = [
            Card.create(
                front="What is the derivative of x²?",
                back="2x"
            ),
            Card.create(
                front="What is the Pythagorean theorem?",
                back="a² + b² = c²"
            ),
            Card.create(
                front="What is the quadratic formula?",
                back="x = (-b ± √(b²-4ac)) / 2a"
            ),
        ]
        math_deck = Deck.create(name="Mathematics", cards=math_cards)
        deck_repo.add(math_deck)
        
        # History Deck
        history_cards = [
            Card.create(
                front="When did World War II end?",
                back="1945"
            ),
            Card.create(
                front="Who was the first President of the United States?",
                back="George Washington"
            ),
        ]
        history_deck = Deck.create(name="World History", cards=history_cards)
        deck_repo.add(history_deck)
        
        # Empty deck for testing
        empty_deck = Deck.create(name="Empty Test Deck", cards=[])
        deck_repo.add(empty_deck)
        
        print(f"    ✓ Created 5 decks")
        print(f"    ✓ Created 14 cards total")
        print(f"    📚 Decks: Spanish, Python, Math, History, Empty")

def main():
    parser = argparse.ArgumentParser(
        description="Initialize Flashcard database with schema and sample data",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create dev database with sample data
  python scripts/db/init_db.py
  
  # Create test database
  python scripts/db/init_db.py --env test
  
  # Force overwrite without prompt
  python scripts/db/init_db.py --force
  
  # Create empty database (no sample data)
  python scripts/db/init_db.py --no-sample-data
        """
    )
    
    parser.add_argument(
        '--env',
        choices=['development', 'test', 'production'],
        default='development',
        help='Environment (default: development)'
    )
    parser.add_argument(
        '--force',
        action='store_true',
        help='Force overwrite without prompting'
    )
    parser.add_argument(
        '--no-sample-data',
        action='store_true',
        help='Skip adding sample data'
    )
    
    args = parser.parse_args()
    
    create_database(
        env=args.env,
        force=args.force,
        with_sample_data=not args.no_sample_data
    )

if __name__ == "__main__":
    main()