from fastapi import FastAPI

# Create the FastAPI application
app = FastAPI(
    title="InvestIQ API",
    description="AI-powered Indian and US stock research platform",
    version="0.1.0"
)


# Root endpoint
@app.get("/")
def home():
    return {
        "message": "Welcome to InvestIQ!",
        "status": "running",
        "markets": ["India", "US"]
    }


# Health-check endpoint
@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }