from bot.database.RedisClient import RedisClient
from bot.services import api, UserService
from bot.database.methods import create, get, update
from bot.misc.env import Stuff
from bot.database.models import user, managerUser

redis_cli_db_0 = RedisClient()


class UserStart:
    __slots__ = ['uid']

    def __init__(self, uid):
        self.uid = uid

    async def _validate_company(self, data):
        # get data company

        # if add
        api_ = api.API(data)
        # company_data = await api.get_company()
        # db.add_head_company

        # db.get_head_company_by_id (param: title)
        # add data in redis if not

    async def _validate_user(self, in_come_data: dict = None):

        if in_come_data:
            # get data in DB
            data = [(item.user_id, item.is_activ, item.role, item.access, item.company_id, item.unit_id)
                    for item in await get.get_user_by_id(self.uid)]
            # сравниваем данные из базы и данные которые пришли

            # DATA USER
            if data:
                # check data
                print(in_come_data)
            else:
                # ROLE
                if self.uid in Stuff.STUFF:
                    role = 1
                else:
                    role = 4

                # check MANAGER
                manager_data = [(item.is_activ, item.role) for item in
                                await get.get_user_by_id(in_come_data["manager_tid"])]

                if manager_data:
                    # check manager data
                    if manager_data[0][1] == 3:
                        # is manager it is ok
                        print(" manager is ok")
                        pass
                    else:
                        # update data role
                        # api request and response data http://url/manager_id(1C_id)
                        api_response = {
                            "name": "Maksim El",
                            "phone": "8-123-123-12-12",
                            "email": "exempl@mail.ru",
                            "role": 3
                        }
                        await update.update_user_by_id(in_come_data["manager_tid"], api_response)
                        redis_cli_db_0.set_user_data(in_come_data["manager_tid"], api_response)
                else:
                    # api request manager id
                    # data get api data manager

                    # create manager with data api response
                    item = user.User(user_id=in_come_data["manager_tid"], name="Name Manager",
                                     access=0,
                                     role=3, company_id=0, phone="manager phone",
                                     email="manager email",
                                     unit_id=0)
                    # return data and save redis
                    obj_new_manager = UserService.UserService(in_come_data["manager_tid"])
                    manager_data = await obj_new_manager.create_new_user(item)

                # create manager
                item = user.User(user_id=self.uid, name=in_come_data["tg_name"], access=in_come_data["access"],
                                 role=role, company_id=in_come_data["company_id"],
                                 unit_id=in_come_data["unit"])

                obj_new_user = UserService.UserService(self.uid)
                user_data = await obj_new_user.create_new_user(item)

                # add user in table managerUser
                item = managerUser.ManagerUser(self.uid, in_come_data["manager_tid"])
                await obj_new_user.add_link_to_manager(item)
                return user_data, manager_data
        else:
            # check cache USER
            if redis_cli_db_0.get_user_data_by_uid(self.uid):
                data = redis_cli_db_0.get_user_data_by_uid(self.uid)
            else:
                # get data in DB
                data = [(item.user_id, item.is_activ, item.role, item.access, item.company_id, item.unit_id)
                        for item in await get.get_user_by_id(self.uid)]

            if data:
                pass
            else:
                # create base user
                item = user.User(user_id=self.uid)
                await create.add_item(item)

    async def _validate_access(self):
        pass

    async def start(self, context, text: str):

        api_data = {}

        # await context.delete()

        if text:
            id_manager, tg_id_manager, head_company_id, access_unit_company, access_lvl = text.split('_')

            # parse user data
            api_data["manager_id"] = int(id_manager)
            api_data["manager_tid"] = int(tg_id_manager)
            api_data["company_id"] = int(head_company_id)
            api_data["unit"] = int(access_unit_company)
            api_data["access"] = int(access_lvl)
            api_data["tg_name"] = context.from_user.full_name

            # validate user
            user_status = await self._validate_user(api_data)

            # validate company
            # await self._valid_company(api_data)

            # validate access

        else:
            text = "test_obj"

            # validate user
            user_status = await self._validate_user()
            # return data user (company_id)

            # validate company

            # validate access

        await context.bot.send_message(self.uid, text)
