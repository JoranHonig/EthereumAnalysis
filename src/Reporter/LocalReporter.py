from .Reporter import *
from src.Report import Finding

class LocalReporter(Reporter):

    def __init__(self):
        self.findings = []


    def add_finding(self, finding):
        self.findings.append(finding)

