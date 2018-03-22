import time
import logging
from EthereumAnalysis.ContractNotifier.LocalNotifier import LocalNotifier
from EthereumAnalysis.Reporter.LocalReporter import LocalReporter
from EthereumAnalysis.AnalysisRunner.AnalysisRunner import AnalysisRunner
from EthereumAnalysis.AnalysisRunner.MythrilRunner import analyse_mythril

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

        # Start scanning
        self.notifier.scan()

    def _contract_found(self, contract_address, object, source):
        """
        Analyse contract and report findings
        :param contract_address: Address of contract to analyse
        :param source: source name of notifier
        """
        logging.info("Analysis manager got contract with address {} from {}", contract_address, source)
        findings = self.runner.analyse(contract_address)
        # Report findings
        for finding in findings:
            self.reporter.add_finding(finding)


if __name__ == "__main__":

    # Initialize components
    notifier = LocalNotifier('mainnet.infura.io', 443)
    reporter = LocalReporter()
    runner = AnalysisRunner(analysis_functions=[analyse_mythril])

    AnalysisManager(notifier, reporter, runner)

    while True:
        time.sleep(60)
        notifier.scan()