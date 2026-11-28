import logging
from sqlalchemy.exc import SQLAlchemyError
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.models import Company, MarketSymbol
from backend.app.schemas import (
    MarketSymbolCreate,
    MarketSymbolUpdate,
)

logger = logging.getLogger(__name__)

def create_market_symbol(
    db: Session,
    symbol_data: MarketSymbolCreate,
) -> MarketSymbol:

    company = db.get(Company, symbol_data.company_id)

    if company is None:
        raise ValueError("Company not found")

    market_symbol = MarketSymbol(
        company_id=symbol_data.company_id,
        market=symbol_data.market.upper(),
        exchange=symbol_data.exchange.upper(),
        symbol=symbol_data.symbol.upper(),
        currency=symbol_data.currency.upper(),
    )

    try:
        db.add(market_symbol)
        db.commit()
        db.refresh(market_symbol)
        logger.info(
            "Market symbol created successfully: "
            "symbol_id=%s, market=%s, exchange=%s, symbol=%s",
            market_symbol.id,
            market_symbol.market,
            market_symbol.exchange,
            market_symbol.symbol,
        )

    except SQLAlchemyError:
        db.rollback()
        raise

    return market_symbol


def get_market_symbols(
    db: Session,
    company_id: UUID | None = None,
    market: str | None = None,
    exchange: str | None = None,
) -> list[MarketSymbol]:

    filters = []

    if company_id:
        filters.append(MarketSymbol.company_id == company_id)

    if market:
        filters.append(
            MarketSymbol.market == market.upper()
        )

    if exchange:
        filters.append(
            MarketSymbol.exchange == exchange.upper()
        )

    statement = (
        select(MarketSymbol)
        .where(*filters)
        .order_by(MarketSymbol.symbol)
    )

    return list(db.scalars(statement).all())


def get_market_symbol_by_id(
    db: Session,
    symbol_id: UUID,
) -> MarketSymbol | None:

    return db.get(MarketSymbol, symbol_id)


def update_market_symbol(
    db: Session,
    symbol_id: UUID,
    symbol_data: MarketSymbolUpdate,
) -> MarketSymbol | None:

    market_symbol = db.get(MarketSymbol, symbol_id)

    if market_symbol is None:
        return None

    update_data = symbol_data.model_dump(exclude_unset=True)

    # Validate the final market and currency combination.
    final_market = update_data.get(
        "market",
        market_symbol.market,
    )

    final_currency = update_data.get(
        "currency",
        market_symbol.currency,
    )

    expected_currency = {
        "INDIA": "INR",
        "US": "USD",
    }

    required_currency = expected_currency.get(final_market)

    if required_currency is None or final_currency != required_currency:
        raise ValueError(
            f"Invalid currency for market {final_market}"
        )

    for field, value in update_data.items():
        if value is not None:
            setattr(
                market_symbol,
                field,
                value.upper(),
            )

    try:
        db.commit()
        db.refresh(market_symbol)
        logger.info(
            "Market symbol updated successfully: "
            "symbol_id=%s, market=%s, exchange=%s, symbol=%s",
            market_symbol.id,
            market_symbol.market,
            market_symbol.exchange,
            market_symbol.symbol,
        )

    except SQLAlchemyError:
        db.rollback()
        raise

    return market_symbol


def delete_market_symbol(
    db: Session,
    symbol_id: UUID,
) -> bool:

    market_symbol = db.get(MarketSymbol, symbol_id)

    if market_symbol is None:
        return False

    try:
        db.delete(market_symbol)
        db.commit()
        logger.info(
            "Market symbol deleted successfully: "
            "symbol_id=%s, market=%s, exchange=%s, symbol=%s",
            market_symbol.id,
            market_symbol.market,
            market_symbol.exchange,
            market_symbol.symbol,
        )

    except SQLAlchemyError:
        db.rollback()
        raise

    return True