from core.settings.components.redis import REDIS_HOST, REDIS_PASSWORD, REDIS_PORT, REDIS_USER

# CELERY
# https://docs.celeryq.dev/en/latest/index.html
# RUN command: celery -A core worker -l INFO

CELERY_BROKER_URL = f'redis://{REDIS_USER}:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/0'

CELERY_BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 10}

CELERY_ACCEPT_CONTENT = ['application/json']

CELERY_TASK_SERIALIZER = 'json'

CELERY_RESULT_SERIALIZER = 'json'

CELERY_TIMEZONE = TIME_ZONE

CELERY_TASK_TRACK_STARTED = True

CELERY_RESULT_BACKEND = 'django-db'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': f'redis://{REDIS_USER}:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/1',
    }
}

CELERY_CACHE_BACKEND = 'default'