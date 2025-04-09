import logging
import httpx
from app.services.cache import external_cache, get_cache_key
from app.schemas import JobCreate
from app.utils.xml_parser import parse_skills_from_xml

logger = logging.getLogger(__name__)

EXTERNAL_API_URL = "http://external-mock:8080/jobs"

def get_external_jobs(name=None, country=None, salary_min=None) -> list[JobCreate]:
    full_filters = {
        "name": name,
        "country": country,
        "salary_min": salary_min,
    }

    # Always pass all keys to cache key generator (even if None)
    cache_key = get_cache_key(full_filters)

    if cache_key in external_cache:
        logger.info(f"Cache hit for {cache_key}")
        return external_cache[cache_key]

    logger.info(f"Cache miss for {cache_key}. Fetching from external API...")

    # Only non-None params are sent to external API
    query_params = {k: v for k, v in full_filters.items() if v is not None}

    try:
        response = httpx.get(EXTERNAL_API_URL, params=query_params, timeout=5)
        response.raise_for_status()
        data = response.json()
        logger.debug(f"Raw data received from external API: {data}")

        jobs = []
        for country_name, job_entries in data.items():
            for entry in job_entries:
                if not isinstance(entry, list) or len(entry) != 3:
                    logger.warning(f"Skipping malformed entry: {entry}")
                    continue

                try:
                    title, salary, skills_xml = entry
                    skills = parse_skills_from_xml(skills_xml)

                    job = JobCreate(
                        title=title,
                        salary=salary,
                        skills=skills,
                        company="",  # Default or inferred if needed
                        description="",
                        country=country_name,
                    )
                    jobs.append(job)
                except Exception as e:
                    logger.warning(f"Skipping job due to error: {e} | Entry: {entry}")

        logger.info(f"Parsed {len(jobs)} jobs from external source")
        external_cache[cache_key] = jobs
        return jobs

    except Exception as e:
        logger.error(f"Error fetching external jobs: {e}")
        return []

