from bot.database.methods import update, create
from bot.database.RedisClient import RedisClient
from bot.database.models import Company, Ltd, Address, Device

redis_cli = RedisClient()


class CompanyService:
    __slots__ = ["company_id", "unit_id", "uid", "cache"]

    def __init__(self, company_id, unit_id, uid):
        self.company_id = company_id
        self.unit_id = unit_id
        self.uid = uid

    def _create_redis(self, data: dict):
        pass

    def _update_redis(self, data: dict):
        pass

    async def create_company(self, data_company: dict):

        # create head company
        item_company = Company(self.company_id, data_company[self.company_id]["company_title"])
        await create.add_item(item_company)

        # redis cache company_data -> title
        company_value_for_redis = {
            "title": data_company[self.company_id]["company_title"]
        }
        redis_cli.set_company_data(self.company_id, data=company_value_for_redis)

        # create ltd
        for ltd_id, ltd_data in data_company[self.company_id].items():

            if str(ltd_id).isdigit():
                if self.unit_id == ltd_id:
                    access_link_value = {
                        "access_link": f"{self.company_id}:{ltd_id}"
                    }
                    await update.update_user_by_id(self.uid, access_link_value)
                    redis_cli.set_user_data(self.uid, access_link_value)

                # redis cache company_data -> ltd_id
                company_ltd_value_for_redis = {
                    f"{ltd_id}": f"{ltd_id}"
                }
                redis_cli.set_company_data(self.company_id, data=company_ltd_value_for_redis)

                # add -> DB -> table ltds -> field title
                ltd_item = Ltd(ltd_id, self.company_id, ltd_data['ltd_title'])
                await create.add_item(ltd_item)

                # redis cache ltd_data -> title
                ltd_value_for_redis = {
                    f"title": ltd_data['ltd_title']
                }
                redis_cli.set_company_ltd_data(self.company_id, ltd_id, data=ltd_value_for_redis)

                # create address
                for address_id, address_data in ltd_data['address'].items():

                    if self.unit_id == address_id:
                        access_link_value = {
                            "access_link": f"{self.company_id}:{ltd_id}:{address_id}"
                        }
                        await update.update_user_by_id(self.uid, access_link_value)
                        redis_cli.set_user_data(self.uid, access_link_value)

                        # redis cache company_data -> ltd_id
                    ltd_address_value_for_redis = {
                        f"{address_id}": f"{address_id}"
                    }
                    redis_cli.set_company_ltd_data(self.company_id, ltd_id, data=ltd_address_value_for_redis)

                    # add -> DB -> table ltds -> field full_address
                    address_item = Address(address_id, address_data['full_address'], ltd_id)
                    await create.add_item(address_item)

                    # redis cache address_data -> title
                    address_value_for_redis = {
                        f"title": address_data['full_address']
                    }

                    redis_cli.set_company_ltd_address_data(self.company_id, ltd_id,
                                                           address_id, data=address_value_for_redis)

                    # create device
                    for device_id, device_data in address_data['devices'].items():
                        # redis cache address_data -> device_id
                        ltd_address_value_for_redis = {
                            f"{device_id}": f"{device_id}"
                        }

                        redis_cli.set_company_ltd_address_data(self.company_id, ltd_id, address_id,
                                                               data=ltd_address_value_for_redis)

                        # add -> DB -> table ltds -> field device_model, device_type, device_sn
                        device_item = Device(device_id, device_data['device_model'], device_data['device_type'],
                                             device_data['device_sn'], self.company_id, address_id)
                        await create.add_item(device_item)

                        # redis cache device_data -> model, type, sn
                        device_value_for_redis = {
                            f"model": f"{device_data['device_model']}",
                            f"type": f"{device_data['device_type']}",
                            f"sn": f"{device_data['device_sn']}"
                        }

                        redis_cli.set_company_ltd_address_device_data(self.company_id, ltd_id, address_id, device_id,
                                                                      data=device_value_for_redis)

    def update_company(self, new_value):
        pass

    def update_ltd(self, new_value):
        pass

    def update_address(self, new_value):
        pass

    def update_device(self, new_value):
        pass

    async def get_company(self, access_link: str, access):
        parse_access_link = access_link.split(":")
        head_company_data = redis_cli.get_all_company_ltd(parse_access_link[0])

        match access:
            # ACCESS LEVEL 1 - ALL LTD COMPANY ACCESS
            case '1':

                data = {
                    'company_title': head_company_data['title'],
                    'company_id': parse_access_link[0]
                }

                tmp = {}
                for ltd_id in head_company_data.values():
                    if ltd_id.isdigit():
                        tmp[f'{ltd_id}'] = {
                            'ltd_id': ltd_id
                        }

                        ltd = redis_cli.get_company_ltd_data(company_id=parse_access_link[0], ltd_id=ltd_id)
                        tmp[f'{ltd_id}']['title'] = ltd['title']

                data['all_ltd'] = tmp

                return data
            # ACCESS LEVEL 2 - ALL ADDRESS LTD ACCESS
            case '2':
                all_address = redis_cli.get_company_ltd_data(company_id=parse_access_link[0],
                                                             ltd_id=parse_access_link[1])

                data = {
                    'company_title': head_company_data['title'],
                    'ltd_title': all_address['title'],
                    'ltd_id': parse_access_link[1],
                    'company_id': parse_access_link[0]
                }

                tmp = {}
                for address_id in all_address.values():

                    if "00-" in address_id:
                        tmp[f'{address_id}'] = {
                            'address_id': address_id
                        }

                        address = redis_cli.get_company_ltd_address_data(company_id=parse_access_link[0],
                                                                         ltd_id=parse_access_link[1],
                                                                         address_id=address_id)

                        tmp[f'{address_id}']['title'] = address['title']

                data['all_address'] = tmp
                return data
            # ACCESS LEVEL 3 - ALL DEVICE ADDRESS ACCESS
            case '3':
                device = redis_cli.get_company_ltd_address_data(company_id=parse_access_link[0],
                                                                ltd_id=parse_access_link[1],
                                                                address_id=parse_access_link[2])

                ltd_data = redis_cli.get_company_ltd_data(company_id=parse_access_link[0],
                                                          ltd_id=parse_access_link[1])

                data = {
                    'title': device['title'],
                    'ltd_title': ltd_data['title'],
                    'company_id': parse_access_link[0],
                    'company_title': head_company_data['title'],
                    'address_id': parse_access_link[2],
                    'ltd_id': parse_access_link[1],
                    'all_device': {}
                }

                for device_id in device:
                    if "00-" in device_id:
                        tmp = redis_cli.get_company_ltd_address_device_data(company_id=parse_access_link[0],
                                                                            ltd_id=parse_access_link[1],
                                                                            address_id=parse_access_link[2],
                                                                            device_id=device_id)

                        tmp['device_id'] = device_id
                        tmp['title'] = tmp['model']
                        data['all_device'][f'{device_id}'] = tmp

                return data
