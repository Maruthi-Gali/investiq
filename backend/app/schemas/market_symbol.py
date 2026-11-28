from datetime import datetime
from uuid import UUID

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
    model_validator,
)


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

    @field_validator("market", "exchange", "symbol", "currency")
    @classmethod
    def normalize_fields(cls, value: str) -> str:
        return value.strip().upper()

    @field_validator("market")
    @classmethod
    def validate_market(cls, value: str) -> str:
        allowed_markets = {"INDIA", "US"}

        if value not in allowed_markets:
            raise ValueError(
                "Market must be either INDIA or US"
            )

        return value

    @field_validator("currency")
    @classmethod
    def validate_currency(cls, value: str) -> str:
        allowed_currencies = {"INR", "USD"}

        if value not in allowed_currencies:
            raise ValueError(
                "Currency must be either INR or USD"
            )

        return value

    @field_validator("currency")
    @classmethod
    def validate_market_currency(cls, value: str, info):
        market = info.data.get("market")

        expected_currency = {
            "INDIA": "INR",
            "US": "USD",
        }

        if market and value != expected_currency.get(market):
            raise ValueError(
                f"Currency for {market} market must be "
                f"{expected_currency.get(market)}"
            )

        return value


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

    @field_validator("market", "exchange", "symbol", "currency")
    @classmethod
    def normalize_fields(cls, value: str | None) -> str | None:
        if value is None:
            return None

        return value.strip().upper()

    @field_validator("market")
    @classmethod
    def validate_market(cls, value: str | None) -> str | None:
        if value is not None and value not in {"INDIA", "US"}:
            raise ValueError(
                "Market must be either INDIA or US"
            )

        return value

    @field_validator("currency")
    @classmethod
    def validate_currency(cls, value: str | None) -> str | None:
        if value is not None and value not in {"INR", "USD"}:
            raise ValueError(
                "Currency must be either INR or USD"
            )

        return value


    @model_validator(mode="after")
    def validate_market_currency(self):
        if self.market and self.currency:
            expected_currency = {
                "INDIA": "INR",
                "US": "USD",
            }

            if self.currency != expected_currency[self.market]:
                raise ValueError(
                    f"Currency for {self.market} market must be "
                    f"{expected_currency[self.market]}"
                )

        return self


class MarketSymbolResponse(BaseModel):
    id: UUID
    company_id: UUID
    market: str
    exchange: str
    symbol: str
    currency: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)