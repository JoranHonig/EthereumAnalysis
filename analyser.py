#!/usr/bin/env python3
from EthereumAnalysis.AnalysisManager import AnalysisManager
from EthereumAnalysis.ContractNotifier.LocalNotifier import LocalNotifier
from EthereumAnalysis.Reporter.LocalReporter import LocalReporter
from EthereumAnalysis.AnalysisRunner.AnalysisRunner import AnalysisRunner
from EthereumAnalysis.AnalysisRunner.MythrilRunner import analyse_mythril

import time
import logging
import argparse


parser = argparse.ArgumentParser(description='analyser automatically runs analysis on new smart contracts')

local_settings = parser.add_argument_group("Local analysis settings settings")
local_settings.add_argument('-l', action='store_true', help='Use local modules for notification and reporting')
local_settings.add_argument('--rpc-settings', metavar="HOST:PORT", help="Hostname of ethereum rpc interface")
local_settings.add_argument('-i', action='store_true', help="Use infura network")

parser.add_argument('-f', action='store_true', help='Start analysis from genesis block')
parser.add_argument('-d', action='store_true', help='Enable logging')
args = parser.parse_args()
# Enable logging
if args.d:
    logging.basicConfig(level=logging.INFO)

notifier = None
reporter = None

# Initialize local objects
if args.l:
    # Initialize notifier
    notifier = None
    if args.i:
        notifier = LocalNotifier('mainnet.infura.io', 443)
    elif args.rpc_settings:
        raise Exception("Not implemented")
    else:
        raise Exception("Not supported supply at least rpc settings or use infura")

    reporter = LocalReporter()
else:
    raise Exception('Not implemented')

runner = AnalysisRunner(analysis_functions=[analyse_mythril])

if notifier is None or reporter is None or runner is None:
    raise Exception("Invalid setup occurred")

AnalysisManager(notifier, reporter, runner)

while True:
    time.sleep(60)
    notifier.scan()
