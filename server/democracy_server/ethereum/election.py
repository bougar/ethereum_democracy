"""
This modules helps developer to interact with functions of the Smart Contract
deployed on Ethereum.
"""
from web3 import Web3
import logging

DEFAULT_GAS = 3000000


class Ethereum:
    """
    Returns a python representation of a smart contract already deployed in
    Ethereum network
    """
    def __init__(self, provider, contract_address, abi):
        self._logger = logging.getLogger(__name__)
        self.provider = provider
        self.interface = abi
        if Web3.isChecksumAddress(contract_address):
            self.contract_address = contract_address
        else:
            self.contract_address = Web3.toChecksumAddress(contract_address)
        self.web3 = Web3(self.provider)
        self.contract = self.web3.eth.contract(address=self.contract_address,
                                               abi=self.interface)

    def call(self, function, function_args=None, call_kwargs=None):
        """
        Call the specified method on the Contract

        Args:
            function (str): Name of function to call
            function_args (list): List of params to pass in the Contract
                function
            call_kwargs (dict): Dictonary with the options to pass in the
                call
        """
        self._logger.info('Calling function %s of contract %s', function,
                           self.contract_address)
        func = getattr(self.contract.functions, function)
        if function_args is None:
            function_args = list()
        if call_kwargs is None:
            call_kwargs = dict()
        return func(*function_args).call(call_kwargs)

    def send(self, function, account, pkey, function_args=None,
             transact_kwargs=None):
        """
        Send transaction using the provided method

        Args:
            function (str): Name of function to call
            account (str): Account in Hex format from where the transaction
                will be send
            pkey (str): Private key in hex form of the provided account
            function_args (list): List of params to pass in the Contract
                function
            transact_kwargs (dict): Dictonary with the options to pass in the
                transaction
        """
        self._logger.info(
            ('Sending transaction using %s function from account %s in'
             'contract %s'),
            function,
            account,
            self.contract_address
        )
        if function_args is None:
            function_args = list()
        if transact_kwargs is None:
            transact_kwargs = dict()
        nonce = self.web3.eth.getTransactionCount(
            Web3.toChecksumAddress(account.lower())
        )
        transact_kwargs['nonce'] = nonce

        if 'gas' not in transact_kwargs:
            self._logger.info(
                'Gas not provided. Using default value of %s',
                DEFAULT_GAS
            )
            transact_kwargs['gas'] = DEFAULT_GAS

        func = getattr(self.contract.functions, function)(*function_args)
        signed_txn = self.web3.eth.account.sign_transaction(
            func.buildTransaction({
                'nonce': nonce,
                'gas': 3000000
            }),
            pkey
        )
        transaction = self.web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        receipt = self.web3.eth.waitForTransactionReceipt(transaction)
        if receipt['status'] != 1:
            raise ValueError(
                "Failed to send transaction. Status was {} and not 1".format(
                    receipt['status']
                )
            )
