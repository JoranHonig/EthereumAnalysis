#!/usr/bin/env python3
from src.Report.Finding import Finding
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
    eth = EthJsonRpc('mainnet.infura.io', 443, True)
    code = eth.eth_getCode(address)
    contract = ETHContract(code, name=address)
    sym = SymExecWrapper(contract, address)
    issues = fire_lasers(sym)

    # Here we go again
    findings = []
    for issue in issues:
        findings += Finding("Mythril analysis", issue.title, issue.description)

    return findings

# TODO: remove this main func
if __name__ == "__main__":
    analyse_mythril("0x20e836AF82460707652d28D8523E234dfC5048f5")