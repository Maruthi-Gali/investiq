from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class CompanyCreate(BaseModel):
    """
    Schema for creating a company.
    """

    name: str = Field(
        min_length=1,
        max_length=255
    )

    country_code: str = Field(
        min_length=2,
        max_length=2
    )

    sector: str | None = Field(
        default=None,
        max_length=100
    )

    industry: str | None = Field(
        default=None,
        max_length=150
    )

    website: HttpUrl | None = None


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