from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.models import Company, MarketSymbol
from backend.app.schemas import (
    MarketSymbolCreate,
    MarketSymbolUpdate,
)


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

    db.add(market_symbol)
    db.commit()
    db.refresh(market_symbol)

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

    for field, value in update_data.items():
        if value is not None:
            setattr(
                market_symbol,
                field,
                value.upper(),
            )

    db.commit()
    db.refresh(market_symbol)

    return market_symbol


def delete_market_symbol(
    db: Session,
    symbol_id: UUID,
) -> bool:

    market_symbol = db.get(MarketSymbol, symbol_id)

    if market_symbol is None:
        return False

    db.delete(market_symbol)
    db.commit()

    return True