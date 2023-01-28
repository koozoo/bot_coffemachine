from bot.database.RedisClient import RedisClient
from bot.database.methods import get, update
from bot.services.CompanyService import CompanyService
from bot.misc.util import api_response


class CacheService:

    def __init__(self, uid):
        self.redis_cli = RedisClient()
        self.uid = uid

    async def _get_user_data(self):
        return [item.id for item in await get.get_user_by_id(self.uid)]

    async def _create_access_link(self) -> str:
        link = ""

        user_data = [(item.company_id, item.unit_id)
                     for item in await get.get_user_by_id(self.uid)]

        if not [item.id for item in await get.get_company_by_id(user_data[0][0])]:
            api_get_company = api_response     # api request company data

            company = CompanyService(company_id=user_data[0][0], unit_id=user_data[0][1], uid=self.uid)
            await company.create_company(api_get_company)

        link += f"{user_data[0][0]}"

        if link == user_data[0][1]:
            print("CREATE LINK company", link)
            return link

        all_ltd = [ltd.id for ltd in await get.get_all_ltd_by_company_id(user_data[0][0])]

        for ltd_id in all_ltd:

            if ltd_id == user_data[0][1]:
                link += f":{ltd_id}"
                print("CREATE LINK ltd", link)
                return link

            for address_id in [address.id for address in await get.get_all_address_by_ltd_id(ltd_id)]:

                if address_id == user_data[0][1]:
                    link += f":{ltd_id}:{address_id}"
                    print("CREATE LINK address", link)
                    return link

    async def company(self):
        user_data = self._get_user_data()
        print(user_data)
        # get data company
        # company_data = [item.id for item in await get.get_company_by_id(company_id)]

    async def user(self, update_mode=0):
        data = [(item.user_id, item.is_activ, item.role, item.access, item.company_id, item.unit_id,
                 item.access_link)for item in await get.get_user_by_id(self.uid)]

        value = {}

        if data:

            data = data[0]

            if update_mode == 0:
                if data[6] == "null" or data[6] is None:
                    link = await self._create_access_link()
                    value["access_link"] = link
                    await update.update_user_by_id(self.uid, value)

                value['user_id'] = data[0]
                value['is_activ'] = str(data[1])
                value['role'] = data[2]
                value['access'] = data[3]
                value['company_id'] = data[4]
                value['unit_id'] = data[5]

                return await self.process(value=value, callback='user')
            else:
                print("UPDATE REDIS CACHE")
                unit_id_redis = self.redis_cli.get_user_data_by_uid(self.uid)
                print(unit_id_redis)
                if data[5] != unit_id_redis['unit_id']:
                    print("UPDATE LINK")
                    link = await self._create_access_link()
                    value["access_link"] = link
                    await update.update_user_by_id(self.uid, value)

                value['user_id'] = data[0]
                value['is_activ'] = str(data[1])
                value['role'] = data[2]
                value['access'] = data[3]
                value['company_id'] = data[4]
                value['unit_id'] = data[5]

                return await self.process(value=value, callback='user')

    async def brake_list(self):
        pass

    async def process(self, value, callback):
        # update redis data
        self.redis_cli.set_user_data(self.uid, value)

        match callback:
            case 'user':
                return self.redis_cli.get_user_data_by_uid(self.uid)
            case 'access_link':
                pass
            case 'company':
                pass
            case 'break_list':
                pass
