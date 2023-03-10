import logging
from datetime import datetime

from bot.database.main import async_session


async def add_item(obj):
    async with async_session() as s:
        async with s.begin():
            s.add(obj)
            await s.commit()
            logging.info(f"item add in data base {datetime.now()}")


async def add_item_autoincrement(obj):
    async with async_session() as s:
        await s.add(obj)
        await s.flush()
        await s.commit()
        logging.info(f"item add in data base {datetime.now()}")
