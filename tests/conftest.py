import pytest

from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker

from fastapi.testclient import TestClient

from backend.app.core.config import get_settings
from backend.app.core.database import Base, get_db
from backend.app.main import app

# Import models so SQLAlchemy registers their tables.
from backend.app.models import Company, MarketSymbol


settings = get_settings()


TEST_DATABASE_URL = URL.create(
    drivername="postgresql+psycopg",
    username=settings.DATABASE_USER,
    password=settings.DATABASE_PASSWORD,
    host=settings.DATABASE_HOST,
    port=settings.DATABASE_PORT,
    database="investiq_test",
)


test_engine = create_engine(
    TEST_DATABASE_URL,
    pool_pre_ping=True,
)


TestingSessionLocal = sessionmaker(
    bind=test_engine,
    autoflush=False,
    autocommit=False,
    join_transaction_mode="create_savepoint",
)


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """
    Create test database tables before the test session
    and remove them after all tests finish.
    """
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)

    yield

    Base.metadata.drop_all(bind=test_engine)
    test_engine.dispose()


@pytest.fixture
def db_session(setup_test_database):
    """
    Provide an isolated database session for each test.
    """
    connection = test_engine.connect()
    transaction = connection.begin()

    session = TestingSessionLocal(bind=connection)

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture
def client(db_session):
    """
    Provide a FastAPI test client using the test database.
    """

    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()