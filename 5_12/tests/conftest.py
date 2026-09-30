# exercises/test-suite/tests/conftest.py
# L11 — Test fixtures
#
# Your task: Set up an isolated test database and override the get_db dependency.

import pytest
from fastapi.testclient import TestClient

from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool

from sqlalchemy.orm import sessionmaker, Session

from app.database import Base, get_db

from app.main import app


# TODO: Create an in-memory SQLite test engine
# Use StaticPool so the same connection is reused (required for :memory: databases)
# Key concept: We use a SEPARATE in-memory DB for tests so tests never touch
# the real database file.
#
# TEST_DATABASE_URL = "sqlite:///:memory:"
# test_engine = create_engine(
#     TEST_DATABASE_URL,
#     connect_args={"check_same_thread": False},
#     poolclass=StaticPool,
# )
# TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
TEST_DATABASE_URL = "sqlite:///:memory:"
test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False,bind=test_engine)

# TODO: Define a client fixture that:
# 1. Creates all tables in the test DB
# 2. Defines override_get_db() yielding a test session
# 3. Overrides app.dependency_overrides[get_db] = override_get_db
# 4. Yields TestClient(app)
# 5. Cleans up: drop tables, remove override
#
# Key concept — override_dependency pattern:
# FastAPI's dependency_overrides dict lets you replace any dependency with a
# different function for testing. Here we replace get_db (which uses the real
# SQLite file) with override_get_db (which uses :memory:).
# This means ALL endpoints that call Depends(get_db) get the test session instead.

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client():
    """
    Pytest fixture that provides a TestClient with an isolated in-memory DB.

    TODO: Implement using the pattern described above.
    """
   # Create all tables in the test database
    Base.metadata.create_all(bind=test_engine)

    # Override the production database dependency
    app.dependency_overrides[get_db] = override_get_db

    # Provide the test client
    with TestClient(app) as client:
        yield client

    # Clean up after the test
    Base.metadata.drop_all(bind=test_engine)
    app.dependency_overrides.clear()