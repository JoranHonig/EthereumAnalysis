class AnalysisRunner:

    def __init__(self, analysis_functions=[]):
        """
        Constructor for AnalysisRunner
        :param analysis_functions: analysis functions that should be ran
        """
        self.functions = analysis_functions

    def add_analysis_function(self, f):
        """
        Add a function to analyse contracts
        :param f: function to add
        """
        self.functions += f

    def analyse(self, address):
        findings = []
        # run analysis
        for f in self.functions:
            findings += f(address)

        return findings