from app.schemas import Job, JobCreate
from app.storage.memory import (
    add_job, get_job_by_id, update_job_by_id, delete_job_by_id
)


def test_add_and_get_job():
    job = Job(
        id=0,
        title="Backend Developer",
        description="Build APIs",
        company="Backend Inc.",
        salary=90000,
        country="Canada",
        skills=["Go", "Kubernetes"]
    )
    new_job = add_job(job)
    fetched = get_job_by_id(new_job.id)
    assert fetched is not None
    assert fetched.title == "Backend Developer"


def test_update_job_by_id():
    job = Job(
        id=0,
        title="Data Engineer",
        description="Work on pipelines",
        company="Data Corp",
        salary=95000,
        country="UK",
        skills=["Spark"]
    )
    new_job = add_job(job)
    updated = update_job_by_id(new_job.id, JobCreate(
        title="Data Engineer",
        description="Work on pipelines",
        company="Data Corp",
        salary=110000,
        country="UK",
        skills=["Spark"]
    ))
    assert updated is not None
    assert updated.salary == 110000


def test_delete_job_by_id():
    job = Job(
        id=0,
        title="DevOps Engineer",
        description="CI/CD and infra",
        company="Ops Inc.",
        salary=85000,
        country="Germany",
        skills=["AWS"]
    )
    new_job = add_job(job)
    deleted = delete_job_by_id(new_job.id)
    assert deleted is True
    assert get_job_by_id(new_job.id) is None


def test_get_nonexistent_job():
    assert get_job_by_id(9999) is None


def test_update_nonexistent_job():
    updated = update_job_by_id(9999, JobCreate(
        title="Ghost",
        description="Invisible job",
        company="Nowhere",
        salary=0,
        country="Narnia",
        skills=[]
    ))
    assert updated is None


def test_delete_nonexistent_job():
    deleted = delete_job_by_id(9999)
    assert deleted is False

