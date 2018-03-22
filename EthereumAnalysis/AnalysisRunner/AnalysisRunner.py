import logging


class AnalysisRunner:

    def __init__(self, analysis_functions=[]):
        """
        Constructor for AnalysisRunner
        :param analysis_functions: analysis functions that should be ran
        """
        logging.debug("Initializing analysis runner")
        self.functions = analysis_functions

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
        for f in self.functions:
            findings += f(address)

        logging.info("During analysis we found {} issues".format(len(findings)))

        return findings
