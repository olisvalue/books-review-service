import os
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_env(tmp_path, monkeypatch):
    # use test database
    db_file = tmp_path / "test.db"
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{db_file}")
    monkeypatch.setenv("SECRET_KEY", "testsecret")
    monkeypatch.setenv("ALGORITHM", "HS256")
    monkeypatch.setenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1")

def get_token():
    resp = client.post(
        "/token",
        data={"username": "test", "password": "pass"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    return resp.json()["access_token"]

@pytest.fixture(autouse=True)
def create_user():
    client.post("/register", json={"username": "test", "password": "pass"})

@pytest.fixture
def auth_headers():
    token = get_token()
    return {"Authorization": f"Bearer {token}"}

def test_register_and_auth():
    resp = client.post("/register", json={"username": "test2", "password": "pass"})
    assert resp.status_code == 200 or resp.status_code == 400

    resp = client.post(
        "/token",
        data={"username": "test2", "password": "pass"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_reviews_and_recommendations(auth_headers):
    resp = client.post(
        "/reviews",
        headers={**auth_headers, "Content-Type": "application/json"},
        json={"rating": 5, "comment": "good", "book_id": 1}
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["rating"] == 5

    resp = client.get("/recommendations", headers=auth_headers)
    assert resp.status_code == 200
    recs = resp.json().get("recommendations")
    assert isinstance(recs, list)
