from bot.handlers.user.NavigateServiceMenu import NavigateServiceMenu


class BackMenuHub:
    __slots__ = ['context', 'uid', '_storage']

    def __init__(self, context, uid):
        self.context = context
        self.uid = uid
        self._storage = {}

    async def start(self):
        parse_callback = self.context.data.split("_")
        match parse_callback[1]:
            case 'CLOSE':
                await self.context.message.delete()
            case 'BACK':
                nav = NavigateServiceMenu(context=self.context, uid=self.uid)
                await nav.move_back(parse_callback[2])
