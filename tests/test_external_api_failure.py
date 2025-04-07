import httpx
from fastapi.testclient import TestClient
from app.main import app
from app.services.external_sources import external_cache

client = TestClient(app)

def test_external_api_failure(monkeypatch):
    # Clear external cache to avoid false cache hits
    external_cache.clear()

    # Simulate external API failure
    def mock_get(*args, **kwargs):
        raise httpx.RequestError("Simulated external API failure")

    monkeypatch.setattr(httpx, "get", mock_get)

    # Send a search request that triggers internal + external fetch
    response = client.get("/jobs/search", params={"name": "DevOps"})
    assert response.status_code == 200

    json_response = response.json()
    assert "results" in json_response
    assert isinstance(json_response["results"], list)

    # Only internal results should be present; if none, should return an empty list
    for job in json_response["results"]:
        # Assuming external jobs have company "External Inc" in mock
        assert job["company"] != "External Inc"

