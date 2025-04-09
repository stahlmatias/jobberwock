from app.services.cache import external_cache, get_cache_key
from app.schemas import JobCreate
import logging
import httpx

logger = logging.getLogger(__name__)

EXTERNAL_API_URL = "http://external-mock:8080/jobs"

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

        # Handle both dict-by-country and flat list response formats
        if isinstance(data, dict):
            for country_name, job_list in data.items():
                for job in job_list:
                    try:
                        title, salary, skills = job
                        job_dict = {
                            "title": title,
                            "salary": salary,
                            "skills": skills,
                            "company": "",  # Default or inferred if needed
                            "description": "",
                            "country": country_name
                        }
                        jobs.append(JobCreate(**job_dict))
                    except Exception as e:
                        logger.warning(f"Invalid job format in dict: {e}")
        elif isinstance(data, list):
            for job in data:
                try:
                    jobs.append(JobCreate(**job))
                except Exception as e:
                    logger.warning(f"Invalid job format in list: {e}")
        else:
            logger.warning(f"Unexpected data format from external API: {type(data)}")

        external_cache[cache_key] = jobs
        return jobs
    except Exception as e:
        logger.error(f"Error fetching external jobs: {e}")
        return []

