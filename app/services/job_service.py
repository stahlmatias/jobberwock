import logging
from app.schemas import Job, JobCreate
from app.storage.memory import add_job, find_jobs_by_filters
from app.services.external_sources import get_external_jobs

logger = logging.getLogger(__name__)

def create_job(job_data: JobCreate) -> Job:
    return add_job(job_data)

def find_jobs(**filters) -> list[Job]:
    logger.info(f"Finding jobs with filters: {filters}")
    internal = find_jobs_by_filters(**filters)

    try:
        external_raw = get_external_jobs(**filters)
        external = []
        for job in external_raw:
            try:
                external.append(JobCreate(**job))
            except Exception as e:
                logger.warning(f"Skipping invalid external job: {e}")
    except Exception as e:
        logger.error(f"External source failed: {e}")
        external = []

    return internal + external

