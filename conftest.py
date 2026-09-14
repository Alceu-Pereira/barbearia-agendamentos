import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from fastapi.testclient import TestClient

from app.database import Base, get_db
from app.main import app

@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(engine)
    with SessionLocal() as session:
        yield session

    Base.metadata.drop_all(engine)

@pytest.fixture
def client(db_session):
    client = TestClient(app)
    def entrega_sessao():
        yield db_session
    app.dependency_overrides[get_db] = entrega_sessao
    yield client
    app.dependency_overrides.clear()

    