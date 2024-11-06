import redis
from django.conf import settings
# Ab redis_client ko sahi initialize karein
setattr(settings, 'redis_client', redis.StrictRedis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    decode_responses=True
))