from fastapi.testclient import TestClient

URL = "https://example.com/health"


def test_create_monitor_returns_201(client: TestClient) -> None:
    response = client.post("/monitors", json={"url": URL})

    assert response.status_code == 201
    body = response.json()
    assert body["url"] == URL
    assert isinstance(body["id"], int)


def test_create_duplicate_monitor_returns_409(client: TestClient) -> None:
    client.post("/monitors", json={"url": URL})

    response = client.post("/monitors", json={"url": URL})

    assert response.status_code == 409
    assert response.json() == {"detail": "This URL is already monitored"}


def test_get_missing_monitor_returns_404(client: TestClient) -> None:
    response = client.get("/monitors/999999")

    assert response.status_code == 404


def test_create_monitor_with_invalid_url_returns_422(client: TestClient) -> None:
    response = client.post("/monitors", json={"url": "not-a-url"})

    assert response.status_code == 422
