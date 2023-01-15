from bot.database.methods import create, get
from bot.database.RedisClient import RedisClient

redis_cli = RedisClient()


class UserService:

    def __init__(self, uid, ):
        self.uid = uid

    async def create_new_user(self, item):
        await create.add_item(item)

        result = [(it.user_id, item.is_activ, item.role, item.access, item.company_id, item.unit_id)
                  for it in await get.get_user_by_id(self.uid)]
        redis_cli.set_user_data(self.uid, result[0])
        return result[0]

    async def add_link_to_manager(self, item):
        await create.add_item(item)
