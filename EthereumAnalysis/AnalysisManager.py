import logging
import EthereumAnalysis.AnalysisRunner.runners.MythrilRunner
import threading
import asyncio
from multiprocessing.pool import ThreadPool

pool = ThreadPool(4)



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

        self.notifier.callback = self.contract_found
        # self.reporter_lock = threading.RLock()

        # Start scanning
        self.notifier.scan()


    def contract_found(self, contract_address, object, source):
        global pool
        return pool.apply_async(self._contract_found, (contract_address, object, source)).get()

    def _contract_found(self, contract_address, object, source):
        """
        Asynchronous method to analyse contract and report findings
        :param contract_address: Address of contract to analyse
        :param source: source name of notifier
        """
        logging.info("Analysis manager got contract with address {} from {}".format(contract_address, source))
        findings = self.runner.analyse(contract_address)
        # Report findings
        # Only one thread at a time may report findings:
        # self.reporter_lock.acquire()
        try:
            for finding in findings:
                self.reporter.add_finding(finding)
        except:
            # self.reporter_lock.release()
            pass
    @staticmethod
    def funct(add, ob):
        return ob.analyze(add)