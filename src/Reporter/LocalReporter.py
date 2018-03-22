from src.Reporter.Reporter import Reporter
from src.Report.Finding import Finding
import sys
from termcolor import colored, cprint


class LocalReporter(Reporter):

    def __init__(self):
        self.findings = []

    def add_finding(self, finding):
        print("{} Finding source: {}".format(
            colored('[*]', 'green'),
            finding.source
        ))
        print("{} Finding name: {}".format(
            colored('[*]', 'green'),
            finding.name
        ))
        print("{} Contract address: {}".format(
              colored('[*]', 'green'),
              finding.address
        ))
        print("{} Description: \n {}".format(
            colored('[*]', 'green'),
            finding.description
        ))


        # self.findings.append(finding)

    def report(self):
        print("Reporting on {} findings")
        counter = 0
        for finding in self.findings:
            counter += 1
            print("Finding: {}".format(counter))

            print(" Source: {} Name: {}".format(finding.source, finding.name))

            print(" Description: \n {}".format(finding.description))

# if __name__=="__main__":
#     rep = LocalReporter()
#     f = Finding("Me", "super hack", "description", "0x199")
#     rep.add_finding(f)