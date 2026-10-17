import pytest
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.db import SessionLocal, models

@pytest.fixture(scope="session")
def client():
    with TestClient(app) as c:
        yield c

@pytest.fixture
def founder_token(client):
    res = client.post("/api/v1/auth/demo/founder")
    assert res.status_code == 200
    return res.json()["token"]

@pytest.fixture
def worker_token(client):
    res = client.post("/api/v1/auth/demo/worker")
    assert res.status_code == 200
    return res.json()["token"]

@pytest.fixture
def investor_token(client):
    res = client.post("/api/v1/auth/demo/investor")
    assert res.status_code == 200
    return res.json()["token"]
