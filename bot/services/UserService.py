from bot.database.methods import create, get
from bot.database.RedisClient import RedisClient
from bot.services.CacheService import CacheService

redis_cli = RedisClient()


class UserService:
    __slots__ = ["uid", "cache"]

    def __init__(self, uid):
        self.uid = uid
        self.cache = CacheService(uid=uid)

    async def create_new_user(self, item):
        await create.add_item(item)
        await self.cache.user()

    async def update_user(self):
        # update
        await self.cache.user(update_mode=1)

    async def add_link_to_manager(self, item):
        await create.add_item(item)
