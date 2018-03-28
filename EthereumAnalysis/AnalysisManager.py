import logging
import threading

class AnalysisManager:

    def __init__(self, notifier, reporter, runner):
        """
        Constructor for Analysismanager
        :param notifier: Notifier object which finds new contracts
        :param reporter: Reporter object used to output findings
        :param runner: Runner objects which analyses contracts and constructs findings
        """
        self.notifier = notifier
        self.reporter = reporter
        self.runner = runner

        self.notifier.callback = self._contract_found
        self.reporter_lock = threading.Lock()

        # Start scanning
        self.notifier.scan()

    async def _contract_found(self, contract_address, object, source):
        """
        Asynchronous method to analyse contract and report findings
        :param contract_address: Address of contract to analyse
        :param source: source name of notifier
        """
        logging.info("Analysis manager got contract with address {} from {}".format(contract_address, source))
        findings = await self.runner.analyse(contract_address)

        # Report findings
        # Only one thread at a time may report findings:
        self.reporter_lock.acquire()
        try:
            for finding in findings:
                self.reporter.add_finding(finding)
        except:
            self.reporter_lock.release()
