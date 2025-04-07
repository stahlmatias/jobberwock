import os
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_external_jobs(monkeypatch):
    external_url = os.environ.get("EXTERNAL_API_URL", "http://localhost:8081/jobs")
    response = client.get(f"/jobs/search?name=Engineer")
    assert response.status_code == 200
    data = response.json()["results"]
    assert isinstance(data, list)
    assert all("Engineer" in job["title"] for job in data if "title" in job)

