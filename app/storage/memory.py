from typing import List, Optional
from app.schemas import Job, JobCreate

job_db: List[Job] = []
job_id_counter = 1

def add_job(job_data: JobCreate) -> Job:
    global job_id_counter
    job_dict = job_data.model_dump()
    job_dict["id"] = job_id_counter
    job = Job(**job_dict)
    job_id_counter += 1
    job_db.append(job)
    return job

def get_job_by_id(job_id: int) -> Optional[Job]:
    for job in job_db:
        if job.id == job_id:
            return job
    return None

def update_job_by_id(job_id: int, job_data: JobCreate) -> Optional[Job]:
    for i, job in enumerate(job_db):
        if job.id == job_id:
            updated_job = Job(id=job_id, **job_data.model_dump())
            job_db[i] = updated_job
            return updated_job
    return None

def delete_job_by_id(job_id: int) -> bool:
    for job in job_db:
        if job.id == job_id:
            job_db.remove(job)
            return True
    return False

def find_jobs_by_filters(name: str = None, country: str = None, salary_min: int = None) -> List[Job]:
    results = job_db
    if name:
        results = [job for job in results if name.lower() in job.title.lower()]
    if country:
        results = [job for job in results if job.country.lower() == country.lower()]
    if salary_min is not None:
        results = [job for job in results if job.salary >= salary_min]
    return results

