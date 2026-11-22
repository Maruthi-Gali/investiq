from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.schemas import (
    MarketSymbolCreate,
    MarketSymbolUpdate,
    MarketSymbolResponse,
)
from backend.app.services import market_symbol as market_symbol_service


router = APIRouter(
    prefix="/api/v1/market-symbols",
    tags=["Market Symbols"],
)


@router.post(
    "/",
    response_model=MarketSymbolResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_market_symbol(
    symbol_data: MarketSymbolCreate,
    db: Session = Depends(get_db),
):
    try:
        return market_symbol_service.create_market_symbol(
            db=db,
            symbol_data=symbol_data,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This market symbol already exists for this exchange.",
        )


@router.get(
    "/",
    response_model=list[MarketSymbolResponse],
)
def get_market_symbols(
    company_id: UUID | None = None,
    market: str | None = Query(default=None, max_length=20),
    exchange: str | None = Query(default=None, max_length=20),
    db: Session = Depends(get_db),
):
    return market_symbol_service.get_market_symbols(
        db=db,
        company_id=company_id,
        market=market,
        exchange=exchange,
    )


@router.get(
    "/{symbol_id}",
    response_model=MarketSymbolResponse,
)
def get_market_symbol(
    symbol_id: UUID,
    db: Session = Depends(get_db),
):
    market_symbol = market_symbol_service.get_market_symbol_by_id(
        db=db,
        symbol_id=symbol_id,
    )

    if market_symbol is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Market symbol not found.",
        )

    return market_symbol


@router.put(
    "/{symbol_id}",
    response_model=MarketSymbolResponse,
)
def update_market_symbol(
    symbol_id: UUID,
    symbol_data: MarketSymbolUpdate,
    db: Session = Depends(get_db),
):
    try:
        market_symbol = market_symbol_service.update_market_symbol(
            db=db,
            symbol_id=symbol_id,
            symbol_data=symbol_data,
        )

        if market_symbol is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Market symbol not found.",
            )

        return market_symbol

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This market symbol already exists for this exchange.",
        )


@router.delete(
    "/{symbol_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_market_symbol(
    symbol_id: UUID,
    db: Session = Depends(get_db),
):
    deleted = market_symbol_service.delete_market_symbol(
        db=db,
        symbol_id=symbol_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Market symbol not found.",
        )

    return None