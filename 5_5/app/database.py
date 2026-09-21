# exercises/database-notes/app/database.py
# L5 — Database setup
#
# Your task: Configure SQLAlchemy and implement the get_db dependency.

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, DeclarativeBase
from typing import Generator

# Database URL — SQLite stored in a local file
DATABASE_URL = "sqlite:///./notes.db"

#create the engine
engine = create_engine(DATABASE_URL,connect_args={"check_same_thread":False})

#create the session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



class Base(DeclarativeBase):
    pass
    
def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency that provides a database session per request.
"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
