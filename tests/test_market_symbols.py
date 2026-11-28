import uuid


def create_test_company(client):
    """Create a company for market symbol tests."""

    payload = {
        "name": "Market Symbol Test Company",
        "country_code": "US",
        "sector": "Technology",
        "industry": "Software",
        "website": "https://example.com",
    }

    response = client.post(
        "/api/v1/companies/",
        json=payload,
    )

    assert response.status_code == 201

    return response.json()["id"]


def create_test_market_symbol(
    client,
    company_id,
    market="US",
    exchange="NASDAQ",
    symbol="TESTIQ",
    currency="USD",
):
    """Create a market symbol for testing."""

    payload = {
        "company_id": company_id,
        "market": market,
        "exchange": exchange,
        "symbol": symbol,
        "currency": currency,
    }

    response = client.post(
        "/api/v1/market-symbols/",
        json=payload,
    )

    assert response.status_code == 201

    return response.json()

def test_create_market_symbol(client):
    company_id = create_test_company(client)

    payload = {
        "company_id": company_id,
        "market": "US",
        "exchange": "NASDAQ",
        "symbol": "TESTIQ",
        "currency": "USD",
    }

    response = client.post(
        "/api/v1/market-symbols/",
        json=payload,
    )

    assert response.status_code == 201

    data = response.json()

    assert data["symbol"] == "TESTIQ"
    assert data["market"] == "US"
    assert data["exchange"] == "NASDAQ"
    assert data["company_id"] == company_id


def test_duplicate_market_symbol_returns_409(client):
    company_id = create_test_company(client)

    payload = {
        "company_id": company_id,
        "market": "US",
        "exchange": "NASDAQ",
        "symbol": "DUPIQ",
        "currency": "USD",
    }

    first_response = client.post(
        "/api/v1/market-symbols/",
        json=payload,
    )

    assert first_response.status_code == 201

    second_response = client.post(
        "/api/v1/market-symbols/",
        json=payload,
    )

    assert second_response.status_code == 409


def test_market_symbol_with_invalid_company_returns_404(client):
    payload = {
        "company_id": str(uuid.uuid4()),
        "market": "US",
        "exchange": "NASDAQ",
        "symbol": "INVALIDIQ",
        "currency": "USD",
    }

    response = client.post(
        "/api/v1/market-symbols/",
        json=payload,
    )

    assert response.status_code == 404


def test_create_market_symbol_with_invalid_currency_returns_422(client):
    company_id = create_test_company(client)

    payload = {
        "company_id": company_id,
        "market": "US",
        "exchange": "NASDAQ",
        "symbol": "TESTIQ",
        "currency": "USDX",
    }

    response = client.post(
        "/api/v1/market-symbols/",
        json=payload,
    )

    assert response.status_code == 422


def test_create_market_symbol_with_missing_symbol_returns_422(client):
    company_id = create_test_company(client)

    payload = {
        "company_id": company_id,
        "market": "US",
        "exchange": "NASDAQ",
        "currency": "USD",
    }

    response = client.post(
        "/api/v1/market-symbols/",
        json=payload,
    )

    assert response.status_code == 422


def test_get_market_symbol_by_id(client):
    company_id = create_test_company(client)

    created = create_test_market_symbol(
        client,
        company_id,
    )

    response = client.get(
        f"/api/v1/market-symbols/{created['id']}"
    )

    assert response.status_code == 200
    assert response.json()["id"] == created["id"]
    assert response.json()["symbol"] == "TESTIQ"


def test_get_all_market_symbols(client):
    company_id = create_test_company(client)

    create_test_market_symbol(
        client,
        company_id,
        symbol="LISTIQ1",
    )

    create_test_market_symbol(
        client,
        company_id,
        symbol="LISTIQ2",
    )

    response = client.get("/api/v1/market-symbols/")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2


def test_filter_market_symbols_by_market(client):
    us_company_id = create_test_company(client)
    india_company_id = create_test_company(client)

    create_test_market_symbol(
        client,
        us_company_id,
        market="US",
        exchange="NASDAQ",
        symbol="USFILTER",
        currency="USD",
    )

    create_test_market_symbol(
        client,
        india_company_id,
        market="INDIA",
        exchange="NSE",
        symbol="INFILTER",
        currency="INR",
    )

    response = client.get(
        "/api/v1/market-symbols/",
        params={"market": "INDIA"},
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["symbol"] == "INFILTER"


def test_filter_market_symbols_by_exchange(client):
    company_id = create_test_company(client)

    create_test_market_symbol(
        client,
        company_id,
        exchange="NASDAQ",
        symbol="NASDAQIQ",
    )

    create_test_market_symbol(
        client,
        company_id,
        exchange="NYSE",
        symbol="NYSEIQ",
    )

    response = client.get(
        "/api/v1/market-symbols/",
        params={"exchange": "NYSE"},
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["symbol"] == "NYSEIQ"


def test_filter_market_symbols_by_company_id(client):
    first_company_id = create_test_company(client)
    second_company_id = create_test_company(client)

    create_test_market_symbol(
        client,
        first_company_id,
        symbol="COMPANY1",
    )

    create_test_market_symbol(
        client,
        second_company_id,
        symbol="COMPANY2",
    )

    response = client.get(
        "/api/v1/market-symbols/",
        params={"company_id": first_company_id},
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["symbol"] == "COMPANY1"
    assert data[0]["company_id"] == first_company_id


def test_update_market_symbol(client):
    company_id = create_test_company(client)

    created = create_test_market_symbol(
        client,
        company_id,
        symbol="OLDIQ",
    )

    response = client.put(
        f"/api/v1/market-symbols/{created['id']}",
        json={
            "symbol": "NEWIQ",
            "exchange": "NYSE",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["symbol"] == "NEWIQ"
    assert data["exchange"] == "NYSE"
    assert data["currency"] == "USD"

def test_delete_market_symbol(client):
    company_id = create_test_company(client)

    created = create_test_market_symbol(
        client,
        company_id,
    )

    response = client.delete(
        f"/api/v1/market-symbols/{created['id']}"
    )

    assert response.status_code == 204

    get_response = client.get(
        f"/api/v1/market-symbols/{created['id']}"
    )

    assert get_response.status_code == 404


def test_update_nonexistent_market_symbol_returns_404(client):
    nonexistent_id = str(uuid.uuid4())

    response = client.put(
        f"/api/v1/market-symbols/{nonexistent_id}",
        json={"symbol": "NEWIQ"},
    )

    assert response.status_code == 404



def test_india_market_rejects_usd_currency(client):
    company_id = create_test_company(client)

    response = client.post(
        "/api/v1/market-symbols/",
        json={
            "company_id": company_id,
            "market": "INDIA",
            "exchange": "NSE",
            "symbol": "RELIANCE",
            "currency": "USD",
        },
    )

    assert response.status_code == 422



def test_us_market_rejects_inr_currency(client):
    company_id = create_test_company(client)

    response = client.post(
        "/api/v1/market-symbols/",
        json={
            "company_id": company_id,
            "market": "US",
            "exchange": "NASDAQ",
            "symbol": "AAPL",
            "currency": "INR",
        },
    )

    assert response.status_code == 422



def test_updating_market_rejects_incompatible_existing_currency(client):
    company_id = create_test_company(client)

    symbol_id = create_test_market_symbol(
        client,
        company_id,
        market="INDIA",
        exchange="NSE",
        symbol="TCS",
        currency="INR",
    )

    response = client.put(
        f"/api/v1/market-symbols/{symbol_id}",
        json={
            "market": "US",
        },
    )

    assert response.status_code == 422