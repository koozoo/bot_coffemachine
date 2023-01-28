from typing import Union

from aiogram.types import ParseMode

from bot.database.RedisClient import RedisClient
from bot.keyboards.reply import main_menu_auth_user, main_menu_not_auth_user
from bot.services import UserService, ManagerService, CacheService
from bot.database.methods import get, update
from bot.misc.env import Stuff
from bot.database.models import user, managerUser
from bot.misc.settings import ROLE, ACCESS
from bot.misc.util import api_response
from bot.services.CompanyService import CompanyService

redis_cli_db_0 = RedisClient()


class UserStart:
    __slots__ = ['uid', 'context', 'cache']

    def __init__(self, uid, context):
        self.uid = uid
        self.context = context
        self.cache = CacheService.CacheService(uid=uid)

    async def _validate_company(self, company_id, unit_id):
        # get data company
        company_data = [item.id for item in await get.get_company_by_id(company_id)]

        if company_data:
            print("VALIDATE COMPANY IN DB")
        else:
            api_r = api_response
            print('create_company')
            company = CompanyService(company_id=company_id, unit_id=unit_id, uid=self.uid)
            await company.create_company(api_r)

    async def _check_user_in_cache(self):

        # check cache USER
        if redis_cli_db_0.get_user_data_by_uid(self.uid):
            data = redis_cli_db_0.get_user_data_by_uid(self.uid)
        else:
            data = await self.cache.user()

        return data

    async def _validate_user(self, in_come_data: dict = None):
        result_user_data: Union[dict, list]
        if in_come_data:

            manager = ManagerService.ManagerService(in_come_data['manager_tid'], in_come_data['manager_id'])

            # get data in DB
            data = [(item.user_id, item.is_activ, item.role, item.access, item.company_id, item.unit_id)
                    for item in await get.get_user_by_id(self.uid)]

            if data:

                ################
                # UPDATE BLOCK #
                ################

                if self.uid not in Stuff.ADMINS and data[0][2] != 3:
                    role = 4
                    value = {
                        "role": role
                    }
                    await update.update_user_by_id(self.uid, value)

                if in_come_data["company_id"] != data[0][4]:
                    value = {
                        "company_id": in_come_data['company_id']
                    }
                    await update.update_user_by_id(self.uid, value)

                if in_come_data["unit_id"] != data[0][5]:
                    value = {
                        "unit_id": in_come_data['unit_id']
                    }
                    await update.update_user_by_id(self.uid, value)

                if in_come_data["access"] != data[0][3]:
                    value = {
                        "access": in_come_data['access']
                    }
                    await update.update_user_by_id(self.uid, value)

                # check manager -- ПРОРАБОТАТЬ
                if not await get.get_manager_id_by_id(in_come_data['manager_id']):
                    await manager.create_new_manager()

                # update redis cache
                await self.cache.user(update_mode=1)

                return in_come_data['company_id'], in_come_data['access'], in_come_data["unit_id"]
            else:

                ######################
                # REGISTRATION BLOCK #
                ######################

                # get MANAGER data
                manager_data = [(item.user_id, item.is_activ, item.role, item.access, item.company_id, item.unit_id,
                                 item.name, item.phone, item.email)
                                for item in await get.get_user_by_id(in_come_data["manager_tid"])]

                if manager_data:

                    if manager_data[0][2] == 3:
                        # is manager role 3 it is ok
                        if not redis_cli_db_0.get_user_data_by_uid(in_come_data["manager_tid"]):
                            cache = {
                                "name": str(manager_data[0][6]),
                                "phone": str(manager_data[0][7]),
                                "email": str(manager_data[0][8]),
                                "role": 3
                            }
                            redis_cli_db_0.set_user_data(in_come_data["manager_tid"], cache)

                    else:
                        await manager.update_manager()

                else:
                    await manager.create_new_manager()

                # create user
                # ROLE
                if self.uid in Stuff.STUFF:
                    role = 1
                else:
                    role = 4

                item = user.User(user_id=self.uid, name=in_come_data["tg_name"], access=in_come_data["access"],
                                 role=role, company_id=in_come_data["company_id"],
                                 unit_id=in_come_data["unit_id"])

                new_user = UserService.UserService(self.uid)
                await new_user.create_new_user(item)

                # add user in table managerUser
                item = managerUser.ManagerUser(self.uid, in_come_data["manager_tid"])
                await new_user.add_link_to_manager(item)

                return in_come_data["company_id"], in_come_data["access"], in_come_data["unit_id"]
        else:
            user_data: dict
            user_data = await self._check_user_in_cache()

            if user_data:
                return user_data
            else:
                # create base user
                item = user.User(user_id=self.uid)
                new_base_user = UserService.UserService(self.uid)
                await new_base_user.create_new_user(item)

    def _access_deny(self, context, text=False):
        if text:
            msg = f"Привет, <b>{context.from_user.full_name}</b>\n" \
                  f"ВЫ ВВЕЛИ НЕ КОРЕКТНЫЕ ДАННЫЕ\n\n" \
                  f"если ранее были авторизованы, нажмите /start\n\n"
            return msg
        else:
            msg = f"Привет, <b>{context.from_user.full_name}</b>\n" \
                  f"<b>ДОСТУП ЗАПРЕЩЕН, ОБРАТИТЕСЬ К МЕНЕДЖЕРУ ЗА ИНФОРМАЦИЕЙ.</b>"
            return msg

    async def start(self, request_data: str):
        api_request = {"c70a9097-c68e-4fda-b87d-465af6ab6150": "123124_390666918_00-00002607_9724092472_2",
                       "c07761c5-41e8-44ee-9f9e-65e507637c1d": "145673_390666918_00-00002606_00-00002606_1",
                       "c70a9097-c68e-4fda-b87d-465af6ab6160": "123124_390666918_00-00002607_00-01032152_3",
                       "c70a9097-c68e-4fda-b87d-465af6ab6230": "212121_390666918_00-00003009_00-00003009_1"
                       }

        if request_data:
            try:
                text = api_request[f"{request_data}"]
            except KeyError:
                msg = self._access_deny(context=self.context, text=True)
                await self.context.bot.send_message(self.uid, msg, reply_markup=main_menu_not_auth_user(),
                                                    parse_mode=ParseMode.HTML)
                return {}
        else:
            text = ''

        init_data = {}

        # await self.context.delete()

        if text:
            id_manager, tg_id_manager, head_company_id, unit_id, access = text.split('_')

            # parse user data
            init_data["manager_id"] = int(id_manager)
            init_data["manager_tid"] = int(tg_id_manager)
            init_data["company_id"] = head_company_id
            init_data["unit_id"] = unit_id
            init_data["access"] = int(access)
            init_data["tg_name"] = self.context.from_user.full_name

            # validate user
            await self._validate_user(init_data)

            # validate company
            await self._validate_company(company_id=init_data["company_id"], unit_id=init_data['unit_id'])
            company = CompanyService(company_id=init_data["company_id"], unit_id=init_data['unit_id'], uid=self.uid)
            await company.get_company(init_data["unit_id"], init_data["access"])

            user_data = redis_cli_db_0.get_user_data_by_uid(self.uid)

            # print result
            msg = f"Привет, <b>{self.context.from_user.full_name}</b>\n" \
                  f"<b>Вы авторизованы как</b>: {ROLE[int(user_data['role']) - 1][1]}\n" \
                  f"<b>Права доступа</b>: {ACCESS[int(user_data['access'])][1]}\n\n"

            await self.context.bot.send_message(self.uid, msg, reply_markup=main_menu_auth_user(),
                                                parse_mode=ParseMode.HTML)
        else:

            # validate user
            data = await self._validate_user()

            # validate company
            await self._validate_company(company_id=data["company_id"], unit_id=data["unit_id"])
            company = CompanyService(company_id=data["company_id"], unit_id=data["unit_id"], uid=self.uid)

            company_data = await company.get_company(access_link=data["access_link"], access=data["access"])

            if redis_cli_db_0.get_user_data_by_uid(self.uid):

                user_data = redis_cli_db_0.get_user_data_by_uid(self.uid)

                msg = f"Привет, <b>{self.context.from_user.full_name}</b>\n" \
                      f"<b>Вы авторизованы как</b>: {ROLE[int(user_data['role']) - 1][1]}\n" \
                      f"<b>Права доступа</b>: {ACCESS[int(user_data['access'])][1]}\n\n" \
                      f"<b>Компания:</b> {company_data['company_title']}"

                await self.context.bot.send_message(self.uid, msg, reply_markup=main_menu_auth_user(),
                                                    parse_mode=ParseMode.HTML)
            elif data:
                msg = f"Привет, <b>{self.context.from_user.full_name}</b>\n" \
                      f"<b>Вы авторизованы как</b>: {ROLE[data['role'] - 1][1]}\n" \
                      f"<b>Права доступа</b>: {ACCESS[data['access']][1]}\n\n"

                await self.context.bot.send_message(self.uid, msg, reply_markup=main_menu_auth_user(),
                                                    parse_mode=ParseMode.HTML)
            else:
                msg = self._access_deny(context=self.context, text=False)

                await self.context.bot.send_message(self.uid, msg, reply_markup=main_menu_not_auth_user(),
                                                    parse_mode=ParseMode.HTML)
