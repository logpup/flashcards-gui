# Third-party imports
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Create a SQLite database file named 'app.db' in the current directory
DATABASE_URL = "sqlite:///test_local.db"

# Create the engine
engine = create_engine(DATABASE_URL, echo=True) # echo=True logs SQL queries

# Create a SessionLocal class for database sessions
SessionLocal = sessionmaker(bind=engine)

# Base class for model definitions
Base = declarative_base()