from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery
from bot.handlers.user.UserStart import UserStart
from bot.handlers.user.MainMenuHub import MainMenuHub
from bot.handlers.user.BackMenuHub import BackMenuHub
from bot.handlers.user.NavigateServiceMenu import NavigateServiceMenu


async def cmd_start(message: Message):
    uid = message.from_user.id
    auth = UserStart(uid=uid, context=message)
    await auth.start(message.get_args())


async def main_menu_hub(message: Message):
    uid = message.from_user.id
    hub = MainMenuHub(uid=uid, context=message)
    await hub.start()


async def back_menu_hub(call: CallbackQuery):
    uid = call.from_user.id
    hub = BackMenuHub(uid=uid, context=call)
    await hub.start()


async def navigate_service_menu(call: CallbackQuery):
    uid = call.from_user.id
    navigate = NavigateServiceMenu(uid=uid, context=call)
    await navigate.start()


def register_user_handlers(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands="start")
    dp.register_message_handler(main_menu_hub, lambda msg: msg.text in ["🧑‍🔧 Сервис", "👨‍💼 Менеджер",
                                                                        "📍 Контакты", "👨‍🔧 Сервис"])
    dp.register_callback_query_handler(back_menu_hub, text_contains='BACK')
    dp.register_callback_query_handler(navigate_service_menu, text_contains='NAV_')

