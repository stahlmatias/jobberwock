from fastapi import APIRouter, HTTPException
from typing import List

from app.schemas import Job, JobCreate
from app.services.job_service import (
    find_jobs,
    create_job,
    get_job_by_id,
    update_job_by_id,
    delete_job_by_id,
)

import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/jobs/", status_code=201, response_model=Job)
def create_job_route(job: JobCreate):
    logger.info(f"Creating job: {job}")
    return create_job(job)

@router.get("/jobs/", response_model=List[Job])
def list_jobs():
    logger.info("Listing jobs")
    return find_jobs()

@router.get("/jobs/search")
def search_jobs(name: str = None, salary_min: int = None, salary_max: int = None, country: str = None):
    logger.info(f"Searching jobs with filters: name={name}, salary_min={salary_min}, salary_max={salary_max}, country={country}")
    results = find_jobs(
        name=name,
        salary_min=salary_min,
        salary_max=salary_max,
        country=country,
    )
    return {"results": results}

@router.get("/jobs/{job_id}", response_model=Job)
def get_job(job_id: int):
    job = get_job_by_id(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Not Found")
    return job

@router.put("/jobs/{job_id}", response_model=Job)
def update_job(job_id: int, job_data: JobCreate):
    updated = update_job_by_id(job_id, job_data)
    if updated is None:
        raise HTTPException(status_code=404, detail="Not Found")
    return updated

@router.delete("/jobs/{job_id}", status_code=204)
def delete_job(job_id: int):
    deleted = delete_job_by_id(job_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Not Found")

