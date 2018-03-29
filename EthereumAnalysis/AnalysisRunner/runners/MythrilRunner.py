#!/usr/bin/env python3
import logging

from EthereumAnalysis.Report.Finding import Finding
from mythril.ether.ethcontract import ETHContract
from mythril.rpc.client import EthJsonRpc
from mythril.analysis.symbolic import SymExecWrapper
from mythril.analysis.security import fire_lasers


class MythrilRunner:
    """
    Class containing business logic to apply mythril analysis on smart contracts
    """
    def __init__(self, rpc_settings):
        """
        Constructor for MythrilRunner
        :param rpc_settings: Settings used to connect to rpc interface
        """
        logging.debug("Initializing MythrilRunner")
        # Lets just agree to use ssl
        self.eth = EthJsonRpc(rpc_settings[0], rpc_settings[1], True)

    def analyze(self, address):
        """
        Analyse a contract using mythril
        :param address: Address of contract to analyse
        :return: Findings
        """
        # The followin code is kinda straight from mythril, thanks ;)
        # Setup
        code = self.eth.eth_getCode(address)

        contract = ETHContract(code, name=address)
        sym = SymExecWrapper(contract, address)

        # Starting analysis
        logging.debug("Firing lasers on contract with address: {}".format(address))
        issues = fire_lasers(sym)

        logging.debug("Found {} issues using mythril".format(len(issues)))

        # Build findings
        findings = []
        for issue in issues:
            findings += [
                Finding(
                    "Mythril analysis",
                    issue.title,
                    issue.description,
                    issue.contract,
                    issue.pc,
                    issue.type
                )
            ]

        return findings


def get_runner(rpc_settings):
    """ Creates a mythril runner instance and returns the analyze method"""
    return MythrilRunner(rpc_settings)
