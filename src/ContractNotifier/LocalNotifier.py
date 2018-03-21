from ethjsonrpc import EthJsonRpc
import logging
from .Notifier import *


class LocalNotifier(Notifier):

    def __init__(self, rpc_address, rpc_port):
        logging.info("Initializing local notifier")

        self.rpc_client = EthJsonRpc(rpc_address, rpc_port)

        logging.info("Initialized rpc client")
        logging.info("Geth version: {}", self.rpc_client.web3_clientVersion())

        self.current_block = self.rpc_client.eth_blockNumber()

        logging.info("The ethereum client is currently at block {}", self.current_block)


    # Private functions
    def new_blocks(self):
        return self.rpc_client.eth_blockNumber() - self.current_block