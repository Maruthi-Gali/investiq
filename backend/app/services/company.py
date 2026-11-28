import logging
from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from backend.app.models import Company
from backend.app.schemas import CompanyCreate


logger = logging.getLogger(__name__)


def create_company(
    db: Session,
    company_data: CompanyCreate
) -> Company:
    """
    Create and save a company in the database.
    """

    company = Company(
        name=company_data.name,
        country_code=company_data.country_code.upper(),
        sector=company_data.sector,
        industry=company_data.industry,
        website=(
            str(company_data.website)
            if company_data.website
            else None
        ),
    )

    try:
        db.add(company)
        db.commit()
        db.refresh(company)
        logger.info(
            "Company created successfully: company_id=%s, name=%s",
            company.id,
            company.name,
        )

    except SQLAlchemyError:
        db.rollback()
        raise

    return company


def get_companies(
    db: Session,
    skip: int = 0,
    limit: int = 20,
    search: str | None = None,
    country_code: str | None = None,
    sector: str | None = None,
):
    filters = []

    # Search companies by name
    if search:
        filters.append(
            Company.name.ilike(f"%{search.strip()}%")
        )

    # Filter by country
    if country_code:
        filters.append(
            Company.country_code == country_code.upper()
        )

    # Filter by sector
    if sector:
        filters.append(
            Company.sector.ilike(sector.strip())
        )

    # Count matching companies
    count_statement = (
        select(func.count())
        .select_from(Company)
        .where(*filters)
    )

    total = db.scalar(count_statement) or 0

    # Retrieve paginated companies
    statement = (
        select(Company)
        .where(*filters)
        .order_by(Company.name)
        .offset(skip)
        .limit(limit)
    )

    companies = list(db.scalars(statement).all())

    return {
        "items": companies,
        "total": total,
        "skip": skip,
        "limit": limit,
    }


def get_company_by_id(
    db: Session,
    company_id: UUID
) -> Company | None:
    """
    Retrieve a company using its UUID.
    """

    statement = select(Company).where(
        Company.id == company_id
    )

    return db.scalar(statement)


def delete_company(
    db: Session,
    company_id: UUID
) -> bool:
    """
    Delete a company using its UUID.
    """

    company = get_company_by_id(db, company_id)

    if company is None:
        return False

    try:
        db.delete(company)
        db.commit()
        logger.info(
            "Company deleted successfully: company_id=%s",
            company_id,
        )

    except SQLAlchemyError:
        db.rollback()
        raise

    return True