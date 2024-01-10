from fastapi.testclient import TestClient

from app.main import app


def test_get_restaurants():
    with TestClient(app) as client:
        response = client.get("/restaurants")

    assert response.status_code == 200
    assert len(response.json()) == 20


def test_get_restaurant():
    with TestClient(app) as client:
        response = client.get("/restaurant/456162c4-8dab-4959-8cdd-3777c7ede20d")

    assert response.status_code == 200
    payload = response.json()
    assert payload["name"] == "Burger plaza"


def test_get_restaurant_not_found():
    with TestClient(app) as client:
        response = client.get("/restaurant/this-should-not-exist")

    assert response.status_code == 404
    payload = response.json()
    assert "Restaurant unknown" in payload["detail"]
