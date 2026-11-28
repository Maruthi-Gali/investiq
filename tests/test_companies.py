def test_create_company(client):
    payload = {
        "name": "Test Technologies",
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

    data = response.json()

    assert data["name"] == "Test Technologies"
    assert data["country_code"] == "US"
    assert data["sector"] == "Technology"
    assert "id" in data


def test_get_company_not_found(client):
    import uuid

    nonexistent_id = str(uuid.uuid4())

    response = client.get(
        f"/api/v1/companies/{nonexistent_id}"
    )

    assert response.status_code == 404
    data = response.json()

    assert data["success"] is False
    assert data["error"]["code"] == "HTTP_404"
    assert data["error"]["message"] == "Company not found"
    assert data["error"]["details"] is None

def test_create_company_with_missing_name_returns_422(client):
    payload = {
        "country_code": "US",
        "sector": "Technology",
        "industry": "Software",
    }

    response = client.post(
        "/api/v1/companies/",
        json=payload,
    )

    assert response.status_code == 422
    data = response.json()

    assert data["success"] is False
    assert data["error"]["code"] == "VALIDATION_ERROR"
    assert data["error"]["message"] == "Request validation failed"
    assert isinstance(data["error"]["details"], list)


def test_create_company_with_invalid_country_code_returns_422(client):
    payload = {
        "name": "Invalid Company",
        "country_code": "USA",
        "sector": "Technology",
        "industry": "Software",
    }

    response = client.post(
        "/api/v1/companies/",
        json=payload,
    )

    assert response.status_code == 422


def test_company_search(client):
    payload = {
        "name": "SearchTest Technologies",
        "country_code": "US",
        "sector": "Technology",
        "industry": "Software",
    }

    client.post("/api/v1/companies/", json=payload)

    response = client.get(
        "/api/v1/companies/",
        params={"search": "SearchTest"},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 1
    assert data["items"][0]["name"] == "SearchTest Technologies"


def test_company_pagination(client):
    companies = [
        "Pagination Company A",
        "Pagination Company B",
        "Pagination Company C",
    ]

    for name in companies:
        client.post(
            "/api/v1/companies/",
            json={
                "name": name,
                "country_code": "US",
                "sector": "Technology",
                "industry": "Software",
            },
        )

    response = client.get(
        "/api/v1/companies/",
        params={"skip": 0, "limit": 2},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 3
    assert len(data["items"]) == 2
    assert data["skip"] == 0
    assert data["limit"] == 2