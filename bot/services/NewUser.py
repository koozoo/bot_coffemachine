from bot.database.methods import create, get


class NewUser:

    def __init__(self, uid, ):
        self.uid = uid

    async def create_new_user(self, item):
        await create.add_item(item)
        result = [it.user_id for it in await get.get_user_by_id(self.uid)]
        return result
