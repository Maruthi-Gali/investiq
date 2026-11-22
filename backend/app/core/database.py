from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from collections.abc import Generator

from sqlalchemy.orm import Session

from backend.app.core.config import get_settings


settings = get_settings()


DATABASE_URL = URL.create(
    drivername="postgresql+psycopg",
    username=settings.DATABASE_USER,
    password=settings.DATABASE_PASSWORD,
    host=settings.DATABASE_HOST,
    port=settings.DATABASE_PORT,
    database=settings.DATABASE_NAME,
)


engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    echo=settings.DEBUG
)


SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)


class Base(DeclarativeBase):
    pass


def get_db() -> Generator[Session, None, None]:
    """
    Provide a database session for each API request.
    """

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()