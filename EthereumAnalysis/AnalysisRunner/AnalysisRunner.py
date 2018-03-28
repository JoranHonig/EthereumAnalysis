from EthereumAnalysis.AnalysisRunner import runners
import logging
import pkgutil


class AnalysisRunner:
    """
    AnalysisRunner class is used to manage all separate analysis runners and report their findings
    """
    def __init__(self, rpc_settings):
        """
        Constructor for AnalysisRunner
        :param analysis_functions: analysis functions that should be ran
        """
        logging.debug("Initializing analysis runner")
        self.runners = []

        for loader, name, pkg in pkgutil.walk_packages(runners.__path__):
            logging.info('Adding analysis module with name: {}'.format(name))
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

        findings = []
        # run analysis
        for name, method in self.runners:
            try:
                findings += method(address)
            except Exception as e:
                logging.error("Encountered an exception while analyzing contract with address: {} using runner with "
                              "name: {} \n Exception: {}".format(address, name, str(e)))

        logging.info("During analysis we found {} issues".format(len(findings)))

        return findings
