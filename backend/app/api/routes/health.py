from fastapi import APIRouter

router = APIRouter()


@router.get("/health", tags=["Health"])
def health_check():
    """
    Check whether the InvestIQ API is running.
    """
    return {
        "status": "healthy",
        "application": "InvestIQ"
    }