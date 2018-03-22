import time
import logging


class AnalysisManager:

    def __init__(self, notifier, reporter, interval):
        self.notifier = notifier
        self.reporter = reporter
        self.interval = interval

        self.notifier.callback = self._contract_found

        # Start looping
        self.loop()

    def loop(self):
        time.sleep(self.interval)
        self.notifier.scan()

    def _contract_found(self, contract_address, source):
        logging.info("Analysis manager got contract with address {} from {}", contract_address, source)
        
