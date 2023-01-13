import os
from typing import Final
from dotenv import load_dotenv

load_dotenv()


class TgKeys:
    TOKEN: Final = os.environ.get('TOKEN')


class Stuff:
    ADMIN_EMAIL = os.environ.get('ADMIN_POST')
    ADMINS_EMAIL = [ADMIN_EMAIL]

    STUFF = []

    ADMINS = [233652006]
    MANAGERS = []
    SUPERVISOR = []

    STUFF.extend(ADMINS)
    STUFF.extend(MANAGERS)
    STUFF.extend(SUPERVISOR)


class Email:
    EMAIL_LOGIN: Final = os.getenv("EMAIL_LOGIN")
    EMAIL_PWD: Final = os.getenv("EMAIL_PWD")


class DB:
    DATABASE_URL = os.environ.get("DATABASE_URL")
    DATABASE_PORT = os.environ.get("DATABASE_PORT")
    DATABASE_LOGIN = os.environ.get("DATABASE_LOGIN")
    DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD")

    def get_setting(self, table):
        print(self.DATABASE_PASSWORD)
        return f"postgresql+asyncpg://" \
               f"{self.DATABASE_LOGIN}" \
               f"{self.DATABASE_PASSWORD}@" \
               f"{self.DATABASE_URL}:" \
               f"{self.DATABASE_PORT}/" \
               f"{table}"
