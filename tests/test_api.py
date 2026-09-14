"""Tests for the FastAPI app (run without the Functions host)."""
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health() -> None:
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_item_crud() -> None:
    created = client.post("/items", json={"name": "Widget", "price": 9.99})
    assert created.status_code == 201
    item_id = created.json()["id"]

    fetched = client.get(f"/items/{item_id}")
    assert fetched.status_code == 200
    assert fetched.json()["name"] == "Widget"

    updated = client.patch(f"/items/{item_id}", json={"price": 12.5})
    assert updated.status_code == 200
    assert updated.json()["price"] == 12.5

    deleted = client.delete(f"/items/{item_id}")
    assert deleted.status_code == 204

    missing = client.get(f"/items/{item_id}")
    assert missing.status_code == 404
