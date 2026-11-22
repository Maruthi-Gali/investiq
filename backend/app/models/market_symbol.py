import uuid
from datetime import datetime

from sqlalchemy import (
    DateTime,
    ForeignKey,
    String,
    Uuid,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.core.database import Base


class MarketSymbol(Base):

    __tablename__ = "market_symbols"

    __table_args__ = (
        UniqueConstraint(
            "market",
            "exchange",
            "symbol",
            name="uq_market_exchange_symbol",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid.uuid4,
    )

    company_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        ForeignKey("companies.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    market: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    exchange: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    symbol: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        index=True,
    )

    currency: Mapped[str] = mapped_column(
        String(3),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    company = relationship(
        "Company",
        back_populates="market_symbols",
    )