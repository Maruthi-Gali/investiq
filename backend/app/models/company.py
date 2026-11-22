import uuid
from datetime import datetime

from sqlalchemy import DateTime, String, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.core.database import Base


class Company(Base):

    __tablename__ = "companies"

    # Primary key
    id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid.uuid4
    )

    # Company information
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True
    )

    country_code: Mapped[str] = mapped_column(
        String(2),
        nullable=False
    )

    sector: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    industry: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True
    )

    website: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    # Audit timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    market_symbols = relationship(
    "MarketSymbol",
    back_populates="company",
    cascade="all, delete-orphan",
    )