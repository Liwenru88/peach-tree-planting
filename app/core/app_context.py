import asyncio
from app.core.config import settings
from app.core.connect.redis_conn import RedisCache
from app.utils.http_client import AsyncHttpClientApi


class AppContext(object):
    # 限定数据库，redis并发量
    http_client_api: AsyncHttpClientApi
    app_redis_cache: RedisCache
    async_lock: asyncio.Lock

    async def init_app(self):
        self.http_client_api = AsyncHttpClientApi()
        self.app_redis_cache = RedisCache()
        # 异步锁
        self.async_lock = asyncio.Lock()

        await self.app_redis_cache.init_cache(address=settings.APP_REDIS_URI)

    async def close(self):
        await self.http_client_api.close_aiohttp_client()
        await self.app_redis_cache.close()


app_ctx = AppContext()
