import redis


def cache():
    return redis.Redis(
        host="redis-master",
        port=6379
    )