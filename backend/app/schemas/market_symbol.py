from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class MarketSymbolCreate(BaseModel):
    company_id: UUID

    market: str = Field(
        min_length=1,
        max_length=20
    )

    exchange: str = Field(
        min_length=1,
        max_length=20
    )

    symbol: str = Field(
        min_length=1,
        max_length=30
    )

    currency: str = Field(
        min_length=3,
        max_length=3
    )


class MarketSymbolUpdate(BaseModel):
    market: str | None = Field(
        default=None,
        min_length=1,
        max_length=20
    )

    exchange: str | None = Field(
        default=None,
        min_length=1,
        max_length=20
    )

    symbol: str | None = Field(
        default=None,
        min_length=1,
        max_length=30
    )

    currency: str | None = Field(
        default=None,
        min_length=3,
        max_length=3
    )


class MarketSymbolResponse(BaseModel):
    id: UUID
    company_id: UUID
    market: str
    exchange: str
    symbol: str
    currency: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)