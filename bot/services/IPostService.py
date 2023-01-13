import abc


class IPostService:
    __slots__ = ["obj", "text", "method"]

    def __init__(self, obj, text, method):
        self.obj = obj
        self.text = text
        self.method = method

    @abc.abstractmethod
    async def send_for_user(self): pass
    @abc.abstractmethod
    async def send_for_stuff(self): pass