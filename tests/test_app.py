from fastapi.testclient import TestClient

from app.main import app


def test_get_restaurants():
    with TestClient(app) as client:
        response = client.get("/restaurants")

    assert response.status_code == 200
    restaurants = response.json()
    assert len(restaurants) == 20
    assert restaurants[0]["name"] == "Burger plaza"
