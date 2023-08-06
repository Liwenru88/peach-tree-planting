from typing import Optional
from redis.asyncio import Redis, from_url


class RedisCache(object):
    __doc__ = "redis 连接建立"

    def __init__(self):
        self.redis_conn: Optional[Redis] = None

    async def init_cache(self, address: str):
        """
        建立连接
        :return:
        """
        self.redis_conn = await from_url(address, encoding="utf-8", decode_responses=True)

    async def keys(self, pattern):
        return await self.redis_conn.keys(pattern)

    async def set(self, key, value):
        return await self.redis_conn.set(key, value)

    async def get(self, key):
        return await self.redis_conn.get(key)

    async def close(self):
        await self.redis_conn.close()
