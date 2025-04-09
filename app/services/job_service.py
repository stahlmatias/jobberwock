import logging
from typing import List, Optional
from app.schemas import Job, JobCreate

from app.storage.memory import (
    add_job,
    job_db,
    job_id_counter,
    find_jobs_by_filters,
    get_job_by_id as memory_get_job_by_id,
    update_job_by_id as memory_update_job_by_id,
    delete_job_by_id as memory_delete_job_by_id,
)
from app.services.external_sources import get_external_jobs

logger = logging.getLogger(__name__)

def create_job(job_data: JobCreate) -> Job:
    return add_job(job_data)

def find_jobs(**filters) -> List[Job]:
    logger.info(f"Finding jobs with filters: {filters}")

    name = filters.get("name")
    salary_min = filters.get("salary_min")
    salary_max = filters.get("salary_max")
    country = filters.get("country")

    internal_matches = []
    for job in job_db:
        if name and name.lower() not in job.title.lower():
            continue
        if salary_min and job.salary < int(salary_min):
            continue
        if salary_max and job.salary > int(salary_max):
            continue
        if country and country.lower() != job.country.lower():
            continue
        internal_matches.append(job)

    external_job_creates = get_external_jobs(
        name=name,
        country=country,
        salary_min=salary_min,
    )

    external_matches = []
    for i, job in enumerate(external_job_creates):
        try:
            external_matches.append(Job(id=-i - 1, **job.model_dump()))
        except Exception as e:
            logger.error(f"Failed to convert external job to Job: {e}. Job data: {job.dict()}")

    results = internal_matches + external_matches
    logger.info(f"Returning {len(results)} jobs (internal + external)")
    return results

def get_job_by_id(job_id: int) -> Optional[Job]:
    return memory_get_job_by_id(job_id)

def update_job_by_id(job_id: int, job_data: JobCreate) -> Optional[Job]:
    return memory_update_job_by_id(job_id, job_data)

def delete_job_by_id(job_id: int) -> bool:
    return memory_delete_job_by_id(job_id)

