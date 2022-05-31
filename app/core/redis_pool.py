import aioredis

from app.core import config


class RedisPool:
    redis_pool_dict = {}

    def __await__(self):
        self._create_pool()
        return self._create_pool().__await__()

    async def _create_pool(self):
        for i in config.REDIS_DB_LIST:
            pool = aioredis.ConnectionPool.from_url(config.REDIS_URI + f"/{i}", max_connections=10)
            redis = aioredis.Redis(connection_pool=pool)
            self.redis_pool_dict.update({i: redis})
        return self

    def select_db(self, db=52):
        c = self.redis_pool_dict[db]
        if not c:
            raise ValueError('调用的Redis数据库未创建连接池')
        return c

    def close_pool(self):
        for i in self.redis_pool_dict.values():
            i.close()