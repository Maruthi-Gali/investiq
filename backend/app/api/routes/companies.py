from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.schemas import (
    CompanyCreate,
    CompanyResponse,
    CompanyListResponse,
)
from backend.app.services import company as company_service


router = APIRouter(
    prefix="/api/v1/companies",
    tags=["Companies"]
)


@router.post(
    "/",
    response_model=CompanyResponse,
    status_code=status.HTTP_201_CREATED
)
def create_company(
    company_data: CompanyCreate,
    db: Session = Depends(get_db)
):
    return company_service.create_company(
        db=db,
        company_data=company_data
    )


@router.get("/", response_model=CompanyListResponse)
def get_companies(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    search: str | None = Query(default=None, min_length=1, max_length=255),
    country_code: str | None = Query(default=None, min_length=2, max_length=2),
    sector: str | None = Query(default=None, max_length=100),
    db: Session = Depends(get_db),
):
    return company_service.get_companies(
        db=db,
        skip=skip,
        limit=limit,
        search=search,
        country_code=country_code,
        sector=sector,
    )


@router.get(
    "/{company_id}",
    response_model=CompanyResponse
)
def get_company(
    company_id: UUID,
    db: Session = Depends(get_db)
):
    company = company_service.get_company_by_id(
        db=db,
        company_id=company_id
    )

    if company is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found"
        )

    return company


@router.delete(
    "/{company_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_company(
    company_id: UUID,
    db: Session = Depends(get_db)
):
    deleted = company_service.delete_company(
        db=db,
        company_id=company_id
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found"
        )

    return None