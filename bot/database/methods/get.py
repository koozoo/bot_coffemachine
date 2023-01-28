from sqlalchemy.future import select

from bot.database.main import async_session
from bot.database.models import user, managerUser, company, ltd, address


async def get_user_by_id(uid):
    async with async_session() as s:
        q = select(user.User).where(user.User.user_id == uid)
        data = await s.execute(q)
        curr = data.scalars()
    return curr


async def get_manager_id_by_id(uid):
    async with async_session() as s:
        q = select(managerUser.ManagerUser).where(managerUser.ManagerUser.user_id == uid)
        data = await s.execute(q)
        curr = data.scalars()
    return curr


async def get_company_by_id(company_id):
    async with async_session() as s:
        q = select(company.Company).where(company.Company.id == company_id)
        data = await s.execute(q)
        curr = data.scalars()
    return curr


async def get_all_ltd_by_company_id(company_id):
    async with async_session() as s:
        q = select(ltd.Ltd).where(ltd.Ltd.company_id == company_id)
        data = await s.execute(q)
        curr = data.scalars()
    return curr


async def get_all_address_by_ltd_id(ltd_id):
    async with async_session() as s:
        q = select(address.Address).where(address.Address.ltd_id == ltd_id)
        data = await s.execute(q)
        curr = data.scalars()
    return curr

