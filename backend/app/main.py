from fastapi import FastAPI

from backend.app.api.routes import (
    health,
    companies,
    market_symbols,
)
from backend.app.core.config import get_settings


settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    description=(
        "AI-powered investment research platform "
        "for Indian and US stock markets."
    ),
    version=settings.APP_VERSION,
    debug=settings.DEBUG
)


app.include_router(health.router)
app.include_router(companies.router)
app.include_router(market_symbols.router)



@app.get("/", tags=["General"])
def home():
    return {
        "message": f"Welcome to {settings.APP_NAME}!",
        "status": "running",
        "markets": ["India", "US"],
        "version": settings.APP_VERSION,
        "environment": settings.APP_ENV
    }