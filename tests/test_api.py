from sqlalchemy.exc import SQLAlchemyError

def test_home_endpoint(client):
    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "running"
    assert data["markets"] == ["India", "US"]
    assert data["version"] == "0.1.0"


def test_health_check_returns_healthy(client):
    response = client.get("/health")

    assert response.status_code == 200

    assert response.json() == {
        "status": "healthy",
        "application": "InvestIQ",
        "checks": {
            "api": "healthy",
            "database": "healthy",
        },
    }


def test_health_check_returns_503_when_database_unavailable(
    client,
    db_session,
    monkeypatch,
):
    def simulate_database_failure(*args, **kwargs):
        raise SQLAlchemyError("Database connection failed")

    monkeypatch.setattr(
        db_session,
        "execute",
        simulate_database_failure,
    )

    response = client.get("/health")

    assert response.status_code == 503

    assert response.json() == {
        "status": "unhealthy",
        "application": "InvestIQ",
        "checks": {
            "api": "healthy",
            "database": "unhealthy",
        },
    }