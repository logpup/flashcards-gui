# Standard library imports
import os
from pathlib import Path
from typing import Generator

# Third-party imports
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session

# Determine environment
ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')

# Get project root (assuming connection.py is in src/infrastructure/persistence/local/)
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"

# Database path based on environment
DB_PATHS = {
    'development': DATA_DIR / 'dev.db',
    'test': DATA_DIR / 'test.db',
    'production': DATA_DIR / 'local.db'
}

DB_PATH = DB_PATHS.get(ENVIRONMENT, DATA_DIR / 'dev.db')

# Create database URL
DATABASE_URL = f"sqlite:///{DB_PATH}"

# Create the engine
engine = create_engine(
    DATABASE_URL, 
    echo=True,  # Log SQL queries - set to False in production
    connect_args={"check_same_thread": False}  # Needed for SQLite
)

# Create a SessionLocal class for database sessions
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# Base class for model definitions
Base = declarative_base()

# Import ORM schemas to register them with Base
# This must happen after Base is created
def _import_schemas():
    """Import all ORM schemas so they're registered with SQLAlchemy"""
    try:
        from src.infrastructure.persistence.local.schemas.card_schema import CardORM
        from src.infrastructure.persistence.local.schemas.deck_schema import DeckORM
    except ImportError:
        # Schemas not yet created, that's ok during initial setup
        pass

_import_schemas()

@contextmanager
def get_session() -> Generator[Session, None, None]:
    """Context manager for database sessions with automatic commit/rollback."""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

def init_db():
    """Initialize the database by creating all tables."""
    # Ensure data directory exists
    DATA_DIR.mkdir(exist_ok=True)
    
    # Import all ORM models so SQLAlchemy knows about them
    from src.infrastructure.persistence.local.schemas.card_schema import CardORM
    from src.infrastructure.persistence.local.schemas.deck_schema import DeckORM
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    print(f"✓ Database initialized: {DB_PATH}")
    print(f"  Environment: {ENVIRONMENT}")
    
    # Show created tables
    from sqlalchemy import inspect
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print(f"  Tables created: {', '.join(tables)}")

def drop_db():
    """Drop all database tables (useful for testing)"""
    Base.metadata.drop_all(bind=engine)
    print(f"✓ All tables dropped from: {DB_PATH}")

def get_db_info():
    """Get current database information"""
    return {
        'environment': ENVIRONMENT,
        'database_path': str(DB_PATH),
        'database_exists': DB_PATH.exists(),
        'absolute_path': str(DB_PATH.absolute())
    }