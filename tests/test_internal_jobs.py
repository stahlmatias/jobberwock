import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_add_job():
    job_data = {
        "title": "Software Engineer",
        "description": "Develop backend systems",
        "company": "Tech Corp",
        "salary": 120000,
        "country": "USA",
        "skills": ["Python", "Docker"]
    }

    response = client.post("/jobs/", json=job_data)
    assert response.status_code == 201
    assert response.json()["title"] == "Software Engineer"

def test_add_invalid_job():
    invalid_data = {
        "description": "No title provided",
        "company": "Oops Inc.",
        "salary": 90000,
        "country": "Mexico",
        "skills": ["Go"]
    }

    response = client.post("/jobs/", json=invalid_data)
    assert response.status_code == 422

