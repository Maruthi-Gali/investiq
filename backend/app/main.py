from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from backend.app.exceptions.handlers import (
    http_exception_handler,
    validation_exception_handler,
)
from backend.app.api.routes import (
    health,
    companies,
    market_symbols,
)
from backend.app.core.config import get_settings
import logging

from contextlib import asynccontextmanager

from backend.app.core.logging_config import setup_logging


setup_logging()

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("InvestIQ application starting")

    yield

    logger.info("InvestIQ application shutting down")


settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    description=(
        "AI-powered investment research platform "
        "for Indian and US stock markets."
    ),
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    lifespan=lifespan,
)

app.add_exception_handler(
    StarletteHTTPException,
    http_exception_handler,
)

app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler,
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