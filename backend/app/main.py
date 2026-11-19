from fastapi import FastAPI

from backend.app.api.routes import health


app = FastAPI(
    title="InvestIQ API",
    description=(
        "AI-powered investment research platform "
        "for Indian and US stock markets."
    ),
    version="0.1.0"
)


# Register API routers
app.include_router(health.router)


@app.get("/", tags=["General"])
def home():
    return {
        "message": "Welcome to InvestIQ!",
        "status": "running",
        "markets": ["India", "US"],
        "version": "0.1.0"
    }