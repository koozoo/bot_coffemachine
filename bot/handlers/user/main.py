import sys

from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery
from bot.handlers.user.UserStart import UserStart


async def cmd_start(message: Message):
    uid = message.from_user.id
    session = UserStart(uid)
    print(sys.getsizeof(session))
    await session.start(message, message.get_args())


def register_user_handlers(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands="start")

