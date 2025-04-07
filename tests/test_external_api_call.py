from app.services.external_sources import get_external_jobs
from app.schemas import JobCreate

def test_get_external_jobs_from_api():
    jobs = get_external_jobs(name="DevOps")
    assert isinstance(jobs, list)
    assert all(isinstance(job, JobCreate) for job in jobs)

