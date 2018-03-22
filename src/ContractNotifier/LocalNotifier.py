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

    def _new_blocks(self):
        return self.rpc_client.eth_blockNumber() - self.current_block

    def _examine_block(self, number):
        # Gets the block by number, true indicates that we want the entire transactions instead of only hashes
        block = self.rpc_client.eth_getBlockByNumber(number, True)

        logging.info("Examining block with number {}", number)

        transactions = block.transactions

    def _examine_transaction(self, transaction_object):
        to = transaction_object.to

        if to is not None:
            logging.debug("Transaction with hash {} is not a contract creating transaction", transaction_object.hash)
            return

        logging.info("Found contract creating transaction with hash {}", transaction_object.hash)

        transaction_receipt = self.rpc_client.eth_getTransactionReceipt(transaction_object.hash)

        contract_address = transaction_receipt.contractAddress

        logging.info("Found new contract with address {}")

        self.encounter(contract_address, "LocalNotifier")
