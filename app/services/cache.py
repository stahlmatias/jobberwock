from cachetools import TTLCache

external_cache = TTLCache(maxsize=100, ttl=60)

def get_cache_key(filters: dict) -> str:
    # Ensure all expected keys are present, even if None
    default_keys = ["country", "name", "salary_min"]
    key_parts = [f"{k}:{filters.get(k)}" for k in default_keys]
    return "_".join(key_parts)
