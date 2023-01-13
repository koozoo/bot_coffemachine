import redis
import uuid


class RedisClient:

    async def set_user_data(self, uid, data: dict = None):
        async with redis.Redis(host="127.0.0.1", port=6379, db=0) as redis_cli:

            await redis_cli.hset(f"user:{uid}", "uid", uid)

            if data:
                for key, value in data.items():
                    await redis_cli.hset(f"user:{uid}", key=key, value=value)

    async def get_user_data_by_uid(self, uid):
        async with redis.Redis(host="127.0.0.1", port=6379, db=0) as redis_cli:

            data = await redis_cli.hget(f"user:{uid}", "uid", uid)
        return data
