import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.connection import Base, engine, SessionLocal


@pytest.fixture(scope="module")
def test_db():
    test_engine = create_engine('postgresql://postgres:admin123@localhost:5432/Events2024')
    Base.metadata.create_all(bind=test_engine)  # Create the tables in the test database
    test_SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    yield test_SessionLocal
    Base.metadata.drop_all(bind=test_engine)


def test_session(test_db):
    session = test_db()
    assert session is not None

