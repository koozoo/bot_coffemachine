from aiogram.types import ParseMode
from bot.keyboards.inline import service_auth
from bot.services.CompanyService import CompanyService
from bot.database.RedisClient import RedisClient

redis_cli = RedisClient()


class MainMenuHub:
    __slots__ = ['context', 'uid', '_storage']

    def __init__(self, context, uid):
        self.context = context
        self.uid = uid
        self._storage = {}

    async def _get_company_data(self, user_data: dict):

        company = CompanyService(company_id=user_data['company_id'],
                                 unit_id=user_data['unit_id'],
                                 uid=self.uid)
        return await company.get_company(access=user_data['access'],
                                         access_link=user_data['access_link'])

    async def _get_user_data(self):
        return redis_cli.get_user_data_by_uid(self.uid)

    async def _get_manager_data(self):
        # get manager tid
        return redis_cli.get_user_data_by_uid(self.uid) # < - insert tid manager

    async def print_msg(self, text):
        await self.context.bot.send_message(self.uid,
                                            text=text,
                                            reply_markup=service_auth(access=self._storage['user_data']['access'],
                                                                      data=self._storage['company_data']),
                                            parse_mode=ParseMode.HTML)

    async def start(self):
        self._storage['user_data'] = await self._get_user_data()
        self._storage['company_data'] = await self._get_company_data(self._storage['user_data'])
        self._storage['manager'] = {} # get manager data
        # price and info for not auth user

        match self.context.text:

            case "🧑‍🔧 Сервис":
                await self.context.delete()
                match self._storage['user_data']['access']:
                    case '1':

                        if self._storage['user_data']['company_id'] != self._storage['user_data']['unit_id']:
                            text = f"Компания: {self._storage['company_data']['company_title']}\n" \
                                   f"<b>Выбирите адрес из списка</b> 👇"
                        else:
                            text = f"Компания: {self._storage['company_data']['company_title']}\n" \
                                   f"<b>Выбирите Юр.Лицо из списка</b> 👇"
                    case '2':

                        text = f"Компания: {self._storage['company_data']['company_title']}\n" \
                               f"Юр.лицо: {self._storage['company_data']['ltd_title']}\n" \
                               f"<b>Выбирите адрес из списка</b> 👇"
                    case '3':

                        text = f"Компания: {self._storage['company_data']['company_title']}\n" \
                               f"Юр.лицо: {self._storage['company_data']['ltd_title']}\n" \
                               f"Адрес: <b>{self._storage['company_data']['title']}</b>\n\n" \
                               f"<b>Выбирите устройство из списка</b> 👇"

                await self.print_msg(text=text)

            case "👨‍💼 Менеджер":
                await self.context.delete()

            case "📍 Контакты":
                await self.context.delete()

            case "👨‍🔧 Сервис":
                await self.context.delete()
