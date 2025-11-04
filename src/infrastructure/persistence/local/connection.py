# Third-party imports
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session

# Create a SQLite database file named 'app.db' in the current directory
DATABASE_URL = "sqlite:///test_local.db"

# Create the engine
engine = create_engine(DATABASE_URL, echo=True) # echo=True logs SQL queries

# Create a SessionLocal class for database sessions
SessionLocal = sessionmaker(bind=engine)

# Base class for model definitions
Base = declarative_base()

@contextmanager
def get_session() -> Session:
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
    Base.metadata.create_all(bind=engine)

def drop_db():
    """Dropp all database tables (usefule for testing)"""
    Base.metadata.drop_all(bind=engine)