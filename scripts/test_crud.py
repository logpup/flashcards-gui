#!/usr/bin/env python3
"""
Test script to verify CRUD operations
Run this and watch changes in DBeaver!
"""
import sys
import os
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Set environment
os.environ['ENVIRONMENT'] = 'development'

from src.domain.models.card import Card
from src.domain.models.deck import Deck
from src.infrastructure.persistence.local.repositories.card_repository import SqlAlchemyCardRepository
from src.infrastructure.persistence.local.repositories.deck_repository import SqlAlchemyDeckRepository
from src.infrastructure.persistence.local.connection import get_db_info

def print_separator(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def main():
    print_separator("FLASHCARD CRUD TEST")
    
    # Show database info
    db_info = get_db_info()
    print(f"Environment: {db_info['environment']}")
    print(f"Database: {db_info['database_path']}")
    print(f"Exists: {db_info['database_exists']}")
    
    if not db_info['database_exists']:
        print("\n❌ Database not found!")
        print("Run: python scripts/db/init_db.py")
        return
    
    # Initialize repositories
    card_repo = SqlAlchemyCardRepository()
    deck_repo = SqlAlchemyDeckRepository()
    
    # === READ - List all decks ===
    print_separator("READ - All Decks")
    decks = deck_repo.list_all()
    print(f"Found {len(decks)} decks:")
    for deck in decks:
        print(f"  📚 {deck.name} (ID: {deck.id}) - {len(deck.cards)} cards")
    
    # === CREATE - New Deck ===
    print_separator("CREATE - New Deck")
    new_deck = Deck.create(name="Geography")
    
    # Add cards to deck
    card1 = Card.create(
        front="What is the capital of Japan?",
        back="Tokyo"
    )
    card2 = Card.create(
        front="What is the largest ocean?",
        back="Pacific Ocean"
    )
    card3 = Card.create(
        front="What mountain range separates Europe and Asia?",
        back="Ural Mountains"
    )
    
    new_deck.add([card1, card2, card3])
    
    # Save to database
    deck_repo.add(new_deck)
    print(f"✓ Created deck: '{new_deck.name}' with {len(new_deck.cards)} cards")
    print(f"  Deck ID: {new_deck.id}")
    
    # === READ - Get specific deck ===
    print_separator("READ - Get Specific Deck")
    retrieved_deck = deck_repo.get_by_id(str(new_deck.id))
    if retrieved_deck:
        print(f"✓ Retrieved deck: '{retrieved_deck.name}'")
        print(f"  Cards in deck:")
        for card in retrieved_deck.cards:
            print(f"    • {card.front} → {card.back}")
    
    # === UPDATE - Modify deck name ===
    print_separator("UPDATE - Deck Name")
    retrieved_deck.name = "World Geography"
    deck_repo.update(retrieved_deck)
    print(f"✓ Updated deck name to: '{retrieved_deck.name}'")
    
    # === CREATE - Add card to existing deck ===
    print_separator("CREATE - Add Card to Deck")
    new_card = Card.create(
        front="What is the longest river in the world?",
        back="Nile River"
    )
    success = deck_repo.add_card_to_deck(str(retrieved_deck.id), new_card)
    if success:
        print(f"✓ Added new card to '{retrieved_deck.name}'")
        print(f"  Card: {new_card.front}")
    
    # === READ - Verify card was added ===
    print_separator("READ - Verify Card Addition")
    updated_deck = deck_repo.get_by_id(str(retrieved_deck.id))
    print(f"Deck '{updated_deck.name}' now has {len(updated_deck.cards)} cards:")
    for i, card in enumerate(updated_deck.cards, 1):
        print(f"  {i}. {card.front}")
    
    # === UPDATE - Modify a card ===
    print_separator("UPDATE - Card Content")
    card_to_update = updated_deck.cards[0]
    card_to_update.back = "Tokyo (東京) - Capital of Japan since 1868"
    card_repo.update(card_to_update)
    print(f"✓ Updated card back:")
    print(f"  Front: {card_to_update.front}")
    print(f"  New Back: {card_to_update.back}")
    
    # === READ - All cards ===
    print_separator("READ - All Cards")
    all_cards = card_repo.list_all()
    print(f"Total cards in database: {len(all_cards)}")
    print("Sample cards:")
    for card in all_cards[:5]:
        print(f"  • {card.front[:40]}...")
    
    # === DELETE - Remove a card ===
    print_separator("DELETE - Card")
    card_to_delete = updated_deck.cards[-1]
    deleted = card_repo.delete(str(card_to_delete.id))
    if deleted:
        print(f"✓ Deleted card:")
        print(f"  Front: {card_to_delete.front}")
    
    # === Final summary ===
    print_separator("FINAL SUMMARY")
    final_decks = deck_repo.list_all()
    final_cards = card_repo.list_all()
    print(f"Total Decks: {len(final_decks)}")
    print(f"Total Cards: {len(final_cards)}")
    
    print("\n" + "="*60)
    print("✅ CRUD Operations Complete!")
    print("="*60)
    print("\n📊 Check DBeaver to see all changes!")
    print(f"   Database: {db_info['absolute_path']}")
    print("   (Press F5 in DBeaver to refresh)\n")

if __name__ == "__main__":
    main()