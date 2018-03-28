import asyncio

class Notifier:

    def __initialize__(self):
        self.callback = lambda x, y, z : x

    def encounter(self, address, source=None):
        return asyncio.ensure_future(self.callback(address, self, source))
