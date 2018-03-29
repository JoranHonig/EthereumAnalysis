from EthereumAnalysis.AnalysisRunner import runners
import asyncio
import logging
import pkgutil

class AnalysisRunner:
    """
    AnalysisRunner class is used to manage all separate analysis runners and report their findings
    """
    def __init__(self, rpc_settings):
        """
        Constructor for AnalysisRunner
        :param rpc_settings: rpc settings to use
        """
        logging.debug("Initializing analysis runner")
        self.runners = []

        for loader, name, pkg in pkgutil.walk_packages(runners.__path__):
            logging.debug('Adding analysis module with name: {}'.format(name))
            try:
                self.runners.append((
                     name,
                     loader.find_module(name)
                         .load_module(name)
                         .get_runner(rpc_settings)
                     )
                )
            except Exception as e:
                logging.error("Encountered an exception while initializing runner with name: {} \n Exception: {}".format(name, str(e)))

    def analyse(self, address):
        """
        Analyse contract
        :param address: address of contract to analyse
        :return: findings
        """
        logging.info("Starting analysis of contract at address: {}".format(address))

        tasks = [self._run_analysis_function(name, method, address) for name, method in self.runners]
        result = []

        for findings in tasks:
            result += findings

        logging.info("During analysis we found {} issues".format(len(result)))

        return result

    @staticmethod
    def _run_analysis_function(name, method, address):
        findings = []
        try:
            findings += method.analyze(address)
        except Exception as e:
            logging.error("Encountered an exception while analyzing contract with address: {} using runner with "
                          "name: {} \n Exception: {}".format(address, name, str(e)))
        return findings

if __name__=="__main__":
    logging.basicConfig(level=logging.INFO)
    a = AnalysisRunner(('mainnet.infura.io', 443))
    loop = asyncio.get_event_loop()
    loop.run_until_complete(a.analyse('0x5312804f1b3f872e2fc3a43c7c9e472017e5e351'))

    exit(0)

