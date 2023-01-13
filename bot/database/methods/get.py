from sqlalchemy.future import select

from bot.database.main import async_session
from bot.database.models import user


async def get_user_by_id(uid):
    async with async_session() as s:
        q = select(user.User).where(user.User.user_id == uid)
        data = await s.execute(q)
        curr = data.scalars()
    return curr
