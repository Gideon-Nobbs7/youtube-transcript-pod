import redis


def cache():
    return redis.Redis(
        host="redis",
        port=6379
    )