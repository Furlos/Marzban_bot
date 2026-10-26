"""Authenticated API contract tests; no real Marzban credentials required."""
import os

from fastapi.testclient import TestClient

from src.api import get_service
from src.main import app


class FakeService:
    async def create_user(self, telegram_id, expire_days, limit_traffic_gb):
        return {
            "username": telegram_id,
            "expire_days": expire_days,
            "data_limit_gb": limit_traffic_gb,
        }

    async def get_user(self, telegram_id):
        return {"username": telegram_id, "status": "active"}

    async def update_user(self, telegram_id, limit_traffic_gb=None, expire_days=None):
        return {"username": telegram_id, "traffic_gb": limit_traffic_gb, "days": expire_days}


def setup_function():
    os.environ["INTERNAL_API_KEY"] = "test-internal-key"
    app.dependency_overrides[get_service] = lambda: FakeService()


def teardown_function():
    app.dependency_overrides.clear()
    os.environ.pop("INTERNAL_API_KEY", None)


client = TestClient(app)


def test_health_is_public():
    assert client.get("/health").json() == {"status": "ok"}


def test_missing_internal_auth_is_rejected():
    assert client.get("/users/123").status_code == 401


def test_invalid_internal_auth_is_rejected():
    assert client.get("/users/123", headers={"X-Internal-Token": "wrong"}).status_code == 401


def test_get_user_by_path_id():
    resp = client.get("/users/123", headers={"X-Internal-Token": "test-internal-key"})
    assert resp.status_code == 200
    assert resp.json()["username"] == "123"


def test_update_user_by_path_id():
    resp = client.put(
        "/users/123",
        json={"traffic_gb": 20, "expire_days": 30},
        headers={"X-Internal-Token": "test-internal-key"},
    )
    assert resp.status_code == 200
    assert resp.json() == {"username": "123", "traffic_gb": 20, "days": 30}


def test_create_user_rejects_invalid_days():
    resp = client.post(
        "/users/",
        json={"username": "123", "expire_days": -1, "data_limit_gb": 12},
        headers={"X-Internal-Token": "test-internal-key"},
    )
    assert resp.status_code == 422


def test_create_user_success():
    resp = client.post(
        "/users/",
        json={"username": "123", "expire_days": 7, "data_limit_gb": 12},
        headers={"X-Internal-Token": "test-internal-key"},
    )
    assert resp.status_code == 200
    assert resp.json()["username"] == "123"
