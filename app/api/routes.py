from fastapi import APIRouter, HTTPException
from app.schemas import Job, JobCreate
from app.services.job_service import find_jobs, create_job

from typing import List
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/jobs/", status_code=201)
def create_job_route(job: JobCreate):
    logger.info(f"Creating job: {job}")
    return create_job(job)

@router.get("/jobs/", response_model=List[Job])
def list_jobs():
    logger.info("Listing internal jobs")
    return find_jobs()

@router.get("/jobs/search")
def search_jobs(name: str = None):
    logger.info(f"Searching jobs with name={name}")
    results = find_jobs(name=name)
    return {
        "results": results
    }

