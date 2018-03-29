import asyncio
import concurrent
from multiprocessing import Pool

class Notifier:

    def __initialize__(self):
        self.callback = lambda x, y, z : x


    def encounter(self, address, source=None):
        return self.callback(address, self, source)


