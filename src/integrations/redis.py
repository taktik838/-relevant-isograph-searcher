from typing import Any

import aioredis
from aioredis.util import _NOTSET


REDIS_HOST = 'localhost'
REDIS_PORT = '6379'
REDIS_TECHNICAL_DB = 2
REDIS_CONNECTION = (REDIS_HOST, REDIS_PORT)


class Redis:
    client = None

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

    async def connect(self):
        if not self.client:
            self.client: aioredis.Redis = await aioredis.create_redis_pool(
                REDIS_CONNECTION,
                # db=REDIS_TECHNICAL_DB,
                encoding='utf-8',
            )

    async def close(self):
        if self.client:
            self.client.close()
            await self.client.wait_closed()
            self.client = None

    async def set(self, key: str, value: str, *, expire=0, pexpire=0, exist=None) -> bool:
        return await self.client.set(key, value, expire=expire, pexpire=pexpire, exist=exist)

    async def get(self, key: str, *, encoding=_NOTSET) -> Any:
        return await self.client.get(key, encoding=encoding)

    async def incr(self, key: str) -> bool:
        return await self.client.incr(key)

    async def expire(self, key: str, timeout: int) -> bool:
        return await self.client.expire(key, timeout)

    async def delete(self, key: str) -> bool:
        return await self.client.delete(key)

    async def info(self) -> Any:
        return await self.client.info()

    async def setex(self, key: str, timeout: int, value: str) -> bool:
        return await self.client.setex(key, timeout, value)

    async def keys(self, pattern: str) -> Any:
        return await self.client.keys(pattern)


async def service(app):
    _redis = Redis()
    await _redis.connect()
    app.redis = _redis
    yield
    await app.redis.close()
