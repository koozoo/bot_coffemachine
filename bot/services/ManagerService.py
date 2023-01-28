from bot.database.methods import create, get, update
from bot.database.RedisClient import RedisClient
from bot.database.models.user import User

redis_cli = RedisClient()


class ManagerService:
    __slots__ = ["uid", "original_id"]

    def __init__(self, uid, original_id):
        self.uid = uid
        self.original_id = original_id

    async def create_new_manager(self):
        # api request manager id
        # data get api data manager
        api_response = {
            "name": "Maksim El",
            "phone": "8-123-123-12-12",
            "email": "exempl@mail.ru",
            "role": 3
        }
        # create manager with data api response
        item = User(user_id=self.uid, name=api_response["name"], access=0,
                    role=3, company_id='null', phone=api_response["phone"],
                    email=api_response["email"],
                    unit_id='null', original_id=str(self.original_id), activ=True)
        await create.add_item(item)

        result = [(it.user_id, item.is_activ, item.role, item.access, item.company_id, item.unit_id,
                   item.phone, item.email, item.name, item.original_id)
                  for it in await get.get_user_by_id(self.uid)]
        redis_cli.set_user_data(self.uid, result[0])

    async def get_data_manager_by_id(self):
        pass

    async def update_manager(self):
        # api request and response data http://url/manager_id(1C_id)
        api_response = {
            "name": "Maksim El",
            "phone": "8-123-123-12-12",
            "email": "exempl@mail.ru",
            "role": 3
        }
        await update.update_user_by_id(self.uid, api_response)
        redis_cli.set_user_data(self.uid, api_response)
