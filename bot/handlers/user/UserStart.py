from aiogram.types import Message, CallbackQuery
from bot.database.RedisClient import RedisClient
from bot.services import api, NewUser
from bot.database.methods import create, get
from bot.database.models import user
from bot.misc.env import Stuff

redis_cli = RedisClient()


class UserStart:
    __slots__ = ['uid']

    def __init__(self, uid):
        self.uid = uid

    async def _valid_company(self, data):
        # get data company

        # if add
        api_ = api.API(data)
        # company_data = await api.get_company()
        # db.add_head_company

        # if get
        # db.get_head_company_by_id (param: title)
        # add data in redis if not

    async def _valid_user(self, in_come_data: dict) -> tuple:
        print(in_come_data)
        # - check in db
        data = [(item.is_activ, item.user_id, item.role, item.access,) for item in await get.get_user_by_id(self.uid)]

        if data:
            if data[0][0]:
                return data[0]
            else:
                return tuple(data[0][0])
        else:
            if in_come_data:
                if self.uid not in Stuff().STUFF:
                    role = 4
                else:
                    role = 1
                item = user.User(user_id=self.uid, role=role, access=in_come_data['access_lvl'])
                usr = NewUser.NewUser(self.uid)
                new_user = await usr.create_new_user(item)
                print(new_user)
            # - select role

            return tuple("et")

    async def start(self, context, text: str):

        api_data = {}

        # await context.delete()

        if text:
            id_manager, tg_id_manager, head_company_id, access_unit_company, access_lvl = text.split('_')

            # parse user data
            api_data["manager_id"] = int(id_manager)
            api_data["tg_manager_id"] = int(tg_id_manager)
            api_data["head_company_id"] = int(head_company_id)
            api_data["access_un it_company_id"] = int(access_unit_company)
            api_data["access_lvl"] = int(access_lvl)

            # validate user and select role + access
            user_status = await self._valid_user(api_data)
            print(user_status)
            # validate company in db add/get
            # await self._valid_company(api_data)

        else:
            text = "test_obj"

            # try get data user if not access deny
            # validate user and select role + access
            user_status = await self._valid_user(api_data)
            print(user_status)

            # if user in db check company -> if in db get company and add to redis

            # check user
            # - select unit
            # - select access

        await context.bot.send_message(self.uid, text)

    def __repr__(self):
        return f"{id(self)} {self.uid}"

    def __del__(self):
        print("Объект удален")