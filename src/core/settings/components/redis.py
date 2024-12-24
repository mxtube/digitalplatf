from core.settings.components import env

# REDIS
# https://redis.io
# https://timeweb.cloud/tutorials/redis/ustanovka-i-nastrojka-redis-dlya-raznyh-os

REDIS_HOST = env('REDIS_HOST')

REDIS_USER = env('REDIS_USER')

REDIS_PASSWORD = env('REDIS_PASSWORD')

REDIS_PORT = env('REDIS_PORT')
