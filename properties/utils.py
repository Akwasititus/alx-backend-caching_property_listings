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
