from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from backend.app.core.database import get_db


router = APIRouter()


@router.get("/health", tags=["Health"])
def health_check(db: Session = Depends(get_db)):
    """
    Check API and database health.
    """

    database_status = "healthy"

    try:
        db.execute(text("SELECT 1"))

    except SQLAlchemyError:
        database_status = "unhealthy"

    overall_status = (
        "healthy"
        if database_status == "healthy"
        else "unhealthy"
    )

    response = {
        "status": overall_status,
        "application": "InvestIQ",
        "checks": {
            "api": "healthy",
            "database": database_status,
        },
    }

    if overall_status == "unhealthy":
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content=response,
        )

    return response