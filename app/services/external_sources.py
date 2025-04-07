from app.services.cache import external_cache, get_cache_key
from app.schemas import JobCreate
import logging
import httpx  # 👈 Usamos httpx en lugar de requests

logger = logging.getLogger(__name__)

EXTERNAL_API_URL = "http://jobberwocky-extra-source-v2:3000/jobs"

def get_external_jobs(name=None, country=None, salary_min=None) -> list[JobCreate]:
    filters = {"name": name, "country": country, "salary_min": salary_min}
    cache_key = get_cache_key(filters)

    if cache_key in external_cache:
        logger.info(f"Cache hit for {cache_key}")
        return external_cache[cache_key]

    logger.info(f"Cache miss for {cache_key}. Fetching from external API...")

    try:
        response = httpx.get(EXTERNAL_API_URL, params=filters, timeout=5)
        response.raise_for_status()
        data = response.json()
        jobs = []

        for job_dict in data:
            try:
                jobs.append(JobCreate(**job_dict))  # No tiene ID
            except Exception as e:
                logger.warning(f"Invalid job from external API: {e}")

        external_cache[cache_key] = jobs
        return jobs
    except Exception as e:
        logger.error(f"Error fetching external jobs: {e}")
        return []

