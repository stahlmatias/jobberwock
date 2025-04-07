import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_combined_results():
    internal_job = {
        "title": "DevOps Engineer",
        "description": "Automate things",
        "company": "Cloud Inc.",
        "salary": 50000,
        "country": "Chile",
        "skills": ["CI/CD", "Docker", "Kubernetes"]
    }

    response = client.post("/jobs/", json=internal_job)
    assert response.status_code == 201

    response = client.get("/jobs/search?name=Engineer")
    assert response.status_code == 200
    data = response.json()["results"]
    assert any("Engineer" in job["title"] for job in data)

