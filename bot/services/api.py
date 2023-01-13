import requests


class API:
    __url = "http://127.0.0.1:8000"

    def __init__(self, data: dict):
        self.data = data

    async def get_company(self):
        data = requests.get(self.__url + "/company/" + self.data['company_id'])
        print(data)
        return data

    async def post_data(self):
        requests.post(self.__url, params=self.data)
