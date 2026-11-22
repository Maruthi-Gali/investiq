def test_home_endpoint(client):
    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "running"
    assert data["markets"] == ["India", "US"]
    assert data["version"] == "0.1.0"