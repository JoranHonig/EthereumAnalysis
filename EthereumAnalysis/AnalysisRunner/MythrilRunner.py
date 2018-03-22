#!/usr/bin/env python3
import logging

from EthereumAnalysis.Report.Finding import Finding
from mythril.ether.ethcontract import ETHContract
from mythril.rpc.client import EthJsonRpc
from mythril.analysis.symbolic import SymExecWrapper
from mythril.analysis.security import fire_lasers


def analyse_mythril(address):
    """
    Analyse a contract using mythril
    :param address: Address of contract to analyse
    :return: Findings
    """
    # The followin code is kinda straight from mythril
    # Setup
    logging.debug("Connecting with ethereum rpc to infura")
    # TODO: dont initialize this every time
    eth = EthJsonRpc('mainnet.infura.io', 443, True)
    code = eth.eth_getCode(address)
    contract = ETHContract(code, name=address)
    sym = SymExecWrapper(contract, address)

    # Analysis
    logging.debug("Firing lasers on contract with address: {}".format(address))
    issues = fire_lasers(sym)

    logging.debug("Found {} issues using mythril".format(len(issues)))

    # Build findings
    findings = []
    for issue in issues:
        findings += [Finding("Mythril analysis", issue.title, issue.description, issue.contract)]

    return findings
