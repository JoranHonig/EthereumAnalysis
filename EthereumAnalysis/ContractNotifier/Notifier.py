class Notifier:

    def __initialize__(self):
        self.callback = lambda x, y, z : x

    def encounter(self, address, source=None):
        self.callback(address, self, source)

    def scan(self):
        pass