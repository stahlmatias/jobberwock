from cachetools import TTLCache

external_cache = TTLCache(maxsize=100, ttl=60)

def get_cache_key(filters: dict) -> str:
    # Creamos una clave estable para usar en cache
    return f"country:{filters.get('country')}_name:{filters.get('name')}_salary_min:{filters.get('salary_min')}"

