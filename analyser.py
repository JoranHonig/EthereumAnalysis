#!/usr/bin/env python3
from EthereumAnalysis.AnalysisManager import AnalysisManager

import argparse

parser = argparse.ArgumentParser(description='analyser automatically runs analysis on new smart contracts')

rpc_settings = parser.add_argument_group("rpc settings")
rpc_settings.add_argument('--rpc-settings', metavar="HOST:PORT", help="Hostname of ethereum rpc interface")
rpc_settings.add_argument('-i', action='store_true', help="Use infura network")

parser.add_argument('-f', action='store_true', help='Start analysis from genesis block')

parser.add_argument('-l', action='store_true', help='Use local modules for notification and reporting')

args = parser.parse_args()

