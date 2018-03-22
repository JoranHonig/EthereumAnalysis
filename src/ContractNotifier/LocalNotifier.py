# from ethjsonrpc import EthJsonRpc
from mythril.rpc.client import EthJsonRpc

import logging
from .Notifier import *


class LocalNotifier(Notifier):

    def __init__(self, rpc_address, rpc_port):
        """
        Constructor for LocalNotifier class
        :param rpc_address: Address of ethereum rpc interface
        :param rpc_port: Port of ethereum rpc interface
        :param callback: Callback function to call when a contract is found
        """
        logging.info("Initializing local notifier")

        super().__init__()
        self.rpc_client = EthJsonRpc(rpc_address, rpc_port, True)

        logging.info("Initialized rpc client")
        logging.info("Geth version: {}", self.rpc_client.web3_clientVersion())

        self.current_block = self.rpc_client.eth_blockNumber()

        logging.info("The ethereum client is currently at block {}", self.current_block)

    def scan(self):
        """
        Scan for new blocks and examine them for new contracts
        """
        new_block = self.rpc_client.eth_blockNumber()
        for i in range(self.current_block + 1, new_block + 1):
            self._examine_block(i)

    def _new_blocks(self):
        """
        :return: Amount of new blocks available
        """
        return self.rpc_client.eth_blockNumber() - self.current_block

    def _examine_block(self, number):
        """
        Examine all transactions in a block and report found contracts
        :param number: blocknumber of block to examine
        """
        # Gets the block by number, true indicates that we want the entire transactions instead of only hashes
        block = self.rpc_client.eth_getBlockByNumber(number, True)

        logging.info("Examining block with number {}", number)

        transactions = block['transactions']

        # Examine all transactions
        for transaction in transactions:
            self._examine_transaction(transaction)

    def _examine_transaction(self, transaction_object):
        """
        Examine a transaction and report any found contracts
        :param transaction_object: object from ethjsonrpc describing the transaction
        """
        if transaction_object['to'] is not None:
            logging.debug("Transaction with hash {} is not a contract creating transaction", transaction_object['hash'])
            return

        logging.info("Found contract creating transaction with hash {}", transaction_object['hash'])

        transaction_receipt = self.rpc_client.eth_getTransactionReceipt(transaction_object['hash'])

        contract_address = transaction_receipt['contractAddress']

        logging.info("Found new contract with address {}")

        self.encounter(contract_address, "LocalNotifier")
