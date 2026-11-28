from datetime import datetime
from uuid import UUID

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    HttpUrl,
    field_validator,
)


class CompanyCreate(BaseModel):
    """
    Schema for creating a company.
    """

    name: str = Field(
        min_length=1,
        max_length=255,
    )

    country_code: str = Field(
        min_length=2,
        max_length=2,
        pattern=r"^[A-Za-z]{2}$",
    )

    sector: str | None = Field(
        default=None,
        max_length=100,
    )

    industry: str | None = Field(
        default=None,
        max_length=150,
    )

    website: HttpUrl | None = None

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Company name cannot be empty")

        return value

    @field_validator("country_code")
    @classmethod
    def normalize_country_code(cls, value: str) -> str:
        return value.strip().upper()

    @field_validator("sector", "industry")
    @classmethod
    def normalize_optional_fields(
        cls,
        value: str | None,
    ) -> str | None:

        if value is None:
            return None

        value = value.strip()

        return value or None


class CompanyResponse(BaseModel):
    """
    Schema for returning company information.
    """

    id: UUID
    name: str
    country_code: str
    sector: str | None
    industry: str | None
    website: str | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CompanyListResponse(BaseModel):
    items: list[CompanyResponse]
    total: int
    skip: int
    limit: int