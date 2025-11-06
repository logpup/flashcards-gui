# Standard library imports

import gc
import warnings
import platform

# Third party imports

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, close_all_sessions

# Local application imports

from src.infrastructure.persistence.local.connection import Base


# Silence ResourceWarning only on Windows
if platform.system() == "Windows":
    warnings.filterwarnings("ignore", category=ResourceWarning)


@pytest.fixture(scope="function")
def test_engine():
    """
    Create an in-memory SQLite database for testing.
    Each test gets a fresh database.
    """
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        pool_pre_ping=True,
        echo=False,
    )

    Base.metadata.create_all(bind=engine)

    try:
        yield engine
    finally:
        # Drop tables and fully close out the engine
        close_all_sessions()
        Base.metadata.drop_all(bind=engine)
        engine.dispose(close=True)
        gc.collect()


@pytest.fixture(scope="function")
def test_session(test_engine, monkeypatch):
    """
    Create a test session and monkey-patch the SessionLocal.
    This ensures all repository operations use the test database.
    """
    TestSessionLocal = sessionmaker(
        bind=test_engine,
        autocommit=False,
        autoflush=False
    )
    
    # Monkey-patch the SessionLocal in connection module
    import src.infrastructure.persistence.local.connection as conn
    monkeypatch.setattr(conn, "SessionLocal", TestSessionLocal)
    
    try:
        yield TestSessionLocal
    finally:
         # Drop tables and fully close out the engine
        close_all_sessions()
        TestSessionLocal.close_all()
        test_engine.dispose(close=True)
        gc.collect()


@pytest.fixture(scope="session")
def sample_data():
    """
    Provide sample test data that can be reused across tests.
    Scope is 'session' as this is read-only data.
    """
    return {
        "cards": [
            {"front": "What is Python?", "back": "A programming language"},
            {"front": "What is SQLAlchemy?", "back": "A Python ORM"},
            {"front": "What is pytest?", "back": "A testing framework"},
        ],
        "decks": [
            "Python Basics",
            "Database Design",
            "Testing Fundamentals",
        ]
    }