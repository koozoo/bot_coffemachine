from typing import Union

from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton


def main_menu_auth_user() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    data = ["🧑‍🔧 Сервис", "👨‍💼 Менеджер", "📍 Контакты"]
    kb.row(data[0]).row(data[1], data[2])
    return kb


def main_menu_not_auth_user() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    data = ["👨‍🔧 Сервис", "📍 Контакты"]
    kb.row(data[0]).row(data[1])
    return kb
