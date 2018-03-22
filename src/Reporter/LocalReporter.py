from src.Reporter.Reporter import Reporter
from src.Report import Finding


class LocalReporter(Reporter):

    def __init__(self):
        self.findings = []

    def add_finding(self, finding):
        print(" Source: {} Name: {}".format(finding.source, finding.name))

        print(" Description: \n {}".format(finding.description))

        # self.findings.append(finding)

    def report(self):
        print("Reporting on {} findings")
        counter = 0
        for finding in self.findings:
            counter += 1
            print("Finding: {}".format(counter))

            print(" Source: {} Name: {}".format(finding.source, finding.name))

            print(" Description: \n {}".format(finding.description))
