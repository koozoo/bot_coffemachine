import logging
from datetime import datetime

from sqlalchemy import update
from bot.database.models import user
from bot.database.main import async_session


async def update_user_by_id(uid: int, data: dict):
    async with async_session() as s:
        async with s.begin():
            q = update(
                user.User)\
                .where(user.User.user_id == uid)\
                .values(data)\
                .execution_options(synchronize_session="fetch")
            await s.execute(q)
            await s.commit()
            logging.info(f"item add in data base {datetime.now()}")
