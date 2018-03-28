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
parser.add_argument('--interval', type=int, help='Ethereum polling interval', default=60)
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
        logging.info("Initializing connection with infura network")
        notifier = LocalNotifier('mainnet.infura.io', 443)
    elif args.rpc_settings:
        logging.info("Initializing connection with ethereum rpc interface at {}".format(args.rpc_settings))
        host = args.rpc_settings.split(':')[0]
        port = args.rpc_settings.split(':')[1]
        notifier = LocalNotifier(host, port)
    else:
        print("Use the infura network or use a custom rpc interface")
        exit(0)

    logging.info("Initializing local reporter")
    reporter = LocalReporter()
else:
    print("Non local analysis is not implemented")
    exit(0)

logging.info("Initializing analysis module")
runner = AnalysisRunner(analysis_functions=[analyse_mythril])

if notifier is None or reporter is None or runner is None:
    print("The required components are not correctly initialized")
    exit(0)

logging.info("Setting up Analysis manager")
AnalysisManager(notifier, reporter, runner)

logging.info("Starting scanning loop with interval {} sec".format(args.interval))
while True:
    time.sleep(args.interval)
    notifier.scan()
