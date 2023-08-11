from redis.asyncio import Redis

from config import REDIS_HOST, REDIS_PORT

redis = Redis(host=REDIS_HOST, port=REDIS_PORT, db='3')
