from django.core.cache import cache
from .models import Property

def get_all_properties():
    """Retrieve all properties, with Redis caching for 1 hour."""
    properties = cache.get('all_properties')

    if properties is None:
        print("Cache miss! Fetching from database...")
        properties = list(Property.objects.all().values(
            'id', 'title', 'description', 'price', 'location', 'created_at'
        ))
        cache.set('all_properties', properties, 3600)  # Cache for 1 hour (3600 seconds)
    else:
        print("Cache hit! Loaded from Redis.")

    return properties




logger = logging.getLogger(__name__)

def get_redis_cache_metrics():
    """
    Retrieve and analyze Redis cache hit/miss metrics.
    Returns a dictionary with hits, misses, and hit ratio.
    """
    try:
        redis_conn = get_redis_connection("default")
        info = redis_conn.info()

        hits = info.get("keyspace_hits", 0)
        misses = info.get("keyspace_misses", 0)

        total = hits + misses
        hit_ratio = (hits / total) if total > 0 else 0

        metrics = {
            "hits": hits,
            "misses": misses,
            "hit_ratio": round(hit_ratio, 2)
        }

        logger.info(f"Redis Cache Metrics → Hits: {hits}, Misses: {misses}, Hit Ratio: {metrics['hit_ratio']}")

        return metrics

    except Exception as e:
        logger.error(f"Error fetching Redis metrics: {e}")
        return {"error": str(e)}
