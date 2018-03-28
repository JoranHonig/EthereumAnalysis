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
            self.runners.append(
                loader.find_module(name)
                    .load_module(name)
                    .get_runner(rpc_settings)
            )

    def add_analysis_function(self, f):
        """
        Add a function to analyse contracts
        :param f: function to add
        """
        logging.debug("Added analysis function")
        self.functions += f

    def analyse(self, address):
        """
        Analyse contract
        :param address: address of contract to analyse
        :return: findings
        """
        logging.info("Starting analysis of contract at address: {}".format(address))

        findings = []
        # run analysis
        for f in self.runners:
            findings += f(address)

        logging.info("During analysis we found {} issues".format(len(findings)))

        return findings
