from typing import Union

import redis
import uuid


class RedisClient:
    ################################
    # DB_0 - CACHE                 #
    ################################
    def __init__(self, host="127.0.0.1", port=6379, db=0, password=None, socket_timeout=None):
        self.host = host
        self.port = port
        self.db = db
        self.password = password
        self.socket_timeout = socket_timeout

    def _connect_redis(self):
        return redis.Redis(host=self.host, port=self.port, db=self.db, decode_responses=True)

    def set_user_data(self, uid, data: Union[dict, tuple]):
        with self._connect_redis() as redis_cli:
            if type(data) is dict:
                for key, value in data.items():
                    redis_cli.hset(f"user:{uid}", key=key, value=value)

            elif type(data) is tuple:
                key = ("user_id", "is_activ", "role", "access", "company_id", "unit_id")

                lst = list(zip(key, data))

                for i in lst:
                    key = i[0]

                    if i[1] is None:
                        value = 0
                    else:
                        value = i[1]

                    redis_cli.hset(f"user:{uid}", key=key, value=str(value))

    def get_user_data_by_uid(self, uid):
        with self._connect_redis() as redis_cli:
            data = redis_cli.hgetall(f"user:{uid}")
        return data

    def set_company_data(self, company_id, data: Union[dict, tuple]):
        with self._connect_redis() as redis_cli:
            if type(data) is dict:
                for key, value in data.items():
                    redis_cli.hset(f"company:{company_id}", key=key, value=value)

            elif type(data) is tuple:
                key = ("id", "is_activ", "title", "description", "phone")

                lst = list(zip(key, data))

                for i in lst:
                    key = i[0]

                    if i[1] is None:
                        value = 0
                    else:
                        value = i[1]

                    redis_cli.hset(f"company:{company_id}", key=key, value=str(value))

    def get_company_data(self, company_id):
        with self._connect_redis() as redis_cli:
            data = redis_cli.hgetall(f"company:{company_id}")
            return data

    def get_managers(self, uid):
        with self._connect_redis() as redis_cli:
            data = redis_cli.hgetall(f"manager:{uid}")
        return data

    def set_managers(self, uid, data):
        with self._connect_redis() as redis_cli:
            if type(data) is dict:
                for key, value in data.items():
                    redis_cli.hset(f"manager:{uid}", key=key, value=value)

            elif type(data) is tuple:
                key = ("user_id", "is_activ", "role", "access", "company_id", "unit_id")

                lst = list(zip(key, data))

                for i in lst:
                    key = i[0]

                    if i[1] is None:
                        value = 0
                    else:
                        value = i[1]

                    redis_cli.hset(f"manager:{uid}", key=key, value=str(value))

    def get_supervisor(self, uid):
        with self._connect_redis() as redis_cli:
            data = redis_cli.hgetall(f"supervisor:{uid}")
        return data

    def set_supervisor(self, uid, data):
        with self._connect_redis() as redis_cli:
            if type(data) is dict:
                for key, value in data.items():
                    redis_cli.hset(f"supervisor:{uid}", key=key, value=value)

            elif type(data) is tuple:
                key = ("user_id", "is_activ", "role", "access", "company_id", "unit_id")

                lst = list(zip(key, data))

                for i in lst:
                    key = i[0]

                    if i[1] is None:
                        value = 0
                    else:
                        value = i[1]

                    redis_cli.hset(f"supervisor:{uid}", key=key, value=str(value))
