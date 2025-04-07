import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.external_sources import external_cache, get_cache_key
import httpx

client = TestClient(app)

mock_response = [
    {
        "title": "DevOps Engineer",
        "description": "Automate all the things.",
        "company": "CI/CD Inc",
        "salary": 110000,
        "country": "Germany",
        "skills": ["Docker", "Kubernetes"]
    }
]

def test_cache_saves_result(monkeypatch):
    # Limpiar cache al principio
    external_cache.clear()

    def mock_get(*args, **kwargs):
        class MockResponse:
            def raise_for_status(self): pass
            def json(self): return mock_response
        return MockResponse()

    monkeypatch.setattr(httpx, "get", mock_get)

    params = {"name": "DevOps"}
    response = client.get("/jobs/search", params=params)
    assert response.status_code == 200

    cache_key = get_cache_key({"country": None, "name": "DevOps", "salary_min": None})

    print(f"\nCache keys: {list(external_cache.keys())}")
    print(f"Expected key: {cache_key}")

    assert cache_key in external_cache, f"Expected cache key {cache_key} not found in cache"

