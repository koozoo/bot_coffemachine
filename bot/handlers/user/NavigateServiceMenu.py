from typing import Tuple

from aiogram.types import ParseMode
from bot.keyboards.inline import view_navigate_menu, service_auth
from bot.services.CompanyService import CompanyService
from bot.database.RedisClient import RedisClient

redis_cli = RedisClient()


class NavigateServiceMenu:
    __slots__ = ['context', 'uid', '_storage', 'user_data']

    def __init__(self, context, uid):
        self.context = context
        self.uid = uid
        self._storage = {}
        self.user_data = redis_cli.get_user_data_by_uid(uid)

    async def link_generation(self, link_data: str) -> tuple[list, str]:
        parse_data = link_data.split(":")

        if len(parse_data) == 4:
            link = parse_data
            back_link = f"{parse_data[0]}:{parse_data[1]}:{parse_data[2]}"

            return link, back_link

        elif len(parse_data) == 3:
            link = parse_data
            back_link = f"{parse_data[0]}:{parse_data[1]}"

            return link, back_link

        elif len(parse_data) == 2:
            link = parse_data
            back_link = f"{parse_data[0]}"

            return link, back_link

        elif len(parse_data) == 1:
            link = parse_data
            back_link = ""

            return link, back_link

    async def start(self):
        parse_data = self.context.data.split("_")

        company = CompanyService(self.user_data['company_id'],
                                 self.user_data['unit_id'],
                                 self.uid)

        match parse_data[1]:
            case "ALL":
                pass
            case 'LTD':
                await self.context.message.delete()
                link, back_link = await self.link_generation(parse_data[2])

                data = await company.get_company(access_link=parse_data[2], access='2')

                text = f'Компания: {data["company_title"]}\n' \
                       f'Юр.Лицо: {data["ltd_title"]}\n' \
                       f'<b>Выбирите адрес</b> 👇'

                if self.user_data['access'] == '1':
                    await self.context.bot.send_message(self.uid, text, reply_markup=view_navigate_menu(data=data,
                                                                                                        back_link=back_link))
                else:
                    await self.context.bot.send_message(self.uid, text, reply_markup=view_navigate_menu(data=data))

            case 'ADDRESS':
                await self.context.message.delete()
                link, back_link = await self.link_generation(parse_data[2])

                data = await company.get_company(access_link=parse_data[2], access='3')

                text = f'Компания: {data["company_title"]}\n' \
                       f'Юр.Лицо: {data["ltd_title"]}\n' \
                       f'Адрес: {data["title"]}\n\n' \
                       f'<b>Выбирите устройство</b> 👇'

                if self.user_data['access'] in ['1', '2']:
                    await self.context.bot.send_message(self.uid, text,
                                                        reply_markup=view_navigate_menu(data=data,
                                                                                        back_link=back_link))
                else:
                    await self.context.bot.send_message(self.uid, "text",
                                                        reply_markup=view_navigate_menu(data=data))

            case 'DEVICE':
                await self.context.message.delete()
                link, back_link = await self.link_generation(parse_data[2])

                _link = ":".join(link[:-1])
                device_link = "".join(link[-1])

                raw_data = await company.get_company(access_link=_link, access='3')

                data = raw_data['all_device'][f'{device_link}']

                text = f'Компания: <b>{raw_data["company_title"]}</b>\n' \
                       f'Юр.Лицо: <b>{raw_data["ltd_title"]}</b>\n' \
                       f'Адрес: <b>{raw_data["title"]}</b>\n\n' \
                       f'Данные устройства: \n' \
                       f'ID: <b>{data["device_id"]}</b>\n' \
                       f'Model: <b>{data["model"]}</b>\n' \
                       f'Type: <b>{data["type"]}</b>\n' \
                       f'S/N: <b>{data["sn"]}</b>'

                await self.context.bot.send_message(self.uid, text,
                                                    reply_markup=view_navigate_menu(data=data,
                                                                                    back_link=back_link))

    async def move_back(self, link: str):
        parse_link = await self.link_generation(link_data=link)

        company = CompanyService(self.user_data['company_id'], self.user_data['unit_id'], self.uid)

        if all(parse_link):

            await self.context.message.delete()

            if len(parse_link[0]) == 2:
                if self.user_data['access'] in ['1', '2']:
                    # BACK TO LIST ADDRESS
                    data = await company.get_company(access_link=":".join(parse_link[0]), access='2')

                    text = f"Компания: {data['company_title']}\n" \
                           f"Юр.лицо: {data['ltd_title']}\n" \
                           f"<b>Выбирите адрес из списка</b> 👇"

                    match self.user_data['access']:
                        case '1':
                            await self.context.bot.send_message(self.uid,
                                                                text=text,
                                                                reply_markup=service_auth(
                                                                    access='2',
                                                                    data=data,
                                                                    user_access=self.user_data['access']))
                        case '2':
                            await self.context.bot.send_message(self.uid,
                                                                text=text,
                                                                reply_markup=service_auth(
                                                                    access='2',
                                                                    data=data))
            else:
                # BACK TO ADDRESS

                data = await company.get_company(access_link=":".join(parse_link[0]), access='3')

                text = f"Компания: {data['company_title']}\n" \
                       f"Юр.лицо: {data['ltd_title']}\n" \
                       f"Адрес: <b>{data['title']}</b>\n\n" \
                       f"<b>Выбирите устройство из списка</b> 👇"

                if self.user_data['access'] in ['1', '2']:
                    await self.context.bot.send_message(self.uid,
                                                        text=text,
                                                        reply_markup=service_auth(
                                                            access='3',
                                                            data=data,
                                                            user_access=self.user_data['access']))
                else:
                    await self.context.bot.send_message(self.uid,
                                                        text=text,
                                                        reply_markup=service_auth(
                                                            access='3',
                                                            data=data))

        else:
            # BACK TO LIST LTD
            await self.context.message.delete()

            data = await company.get_company(access_link=self.user_data['access_link'],
                                             access=self.user_data['access'])

            text = f"Компания: {data['company_title']}\n" \
                   f"<b>Выбирите адрес из списка</b> 👇"

            await self.context.bot.send_message(self.uid,
                                                text=text,
                                                reply_markup=service_auth(
                                                    access=self.user_data['access'],
                                                    data=data))
