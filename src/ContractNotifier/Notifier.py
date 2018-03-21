class Notifier:

    def __initialize__(self, callback):
        self.callback = callback

    def encounter(self, address, source=None):
        self.callback(address, self, source)
