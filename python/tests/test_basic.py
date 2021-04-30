# standard imports
import os
import unittest
import json
import logging

# external imports
from chainlib.eth.unittest.ethtester import EthTesterCase
from chainlib.connection import RPCConnection
from chainlib.eth.nonce import RPCNonceOracle
from chainlib.eth.address import to_checksum_address
from chainlib.eth.tx import (
        receipt,
        transaction,
        TxFormat,
        )
from chainlib.eth.contract import (
        abi_decode_single,
        ABIContractType,
        )
from chainlib.eth.nonce import RPCNonceOracle
from chainlib.eth.constant import ZERO_ADDRESS
from giftable_erc20_token import GiftableToken

# local imports
from erc20_single_shot_faucet import Faucet
from erc20_single_shot_faucet.faucet import SingleShotFaucet

logging.basicConfig(level=logging.DEBUG)
logg = logging.getLogger()


class TestFaucet(EthTesterCase):

    def setUp(self):
        super(TestFaucet, self).setUp()
        self.conn = RPCConnection.connect(self.chain_spec, 'default')
        nonce_oracle = RPCNonceOracle(self.accounts[0], self.conn)
        c = SingleShotFaucet(self.chain_spec, signer=self.signer, nonce_oracle=nonce_oracle)
        (tx_hash, o) = c.store_constructor(self.accounts[0])
        r = self.conn.do(o)
        logg.debug('store deployed with hash {}'.format(r))
        
        o = receipt(r)
        r = self.conn.do(o)
        self.store_address = to_checksum_address(r['contract_address'])
        logg.debug('store contract {}'.format(self.store_address))

        ct = GiftableToken(self.chain_spec, signer=self.signer, nonce_oracle=nonce_oracle)
        (tx_hash_hex, o) = ct.constructor(self.accounts[0], 'Foo Token', 'FOO', 6)
        r = self.conn.do(o)
        logg.debug('token deployed with hash {}'.format(r))

        o = receipt(r)
        r = self.conn.do(o)
        self.token_address = to_checksum_address(r['contract_address'])
        logg.debug('token contract {}'.format(self.store_address))

        (tx_hash, o) = c.constructor(self.accounts[0], self.token_address, self.store_address, ZERO_ADDRESS, self.accounts[1])
        r = self.conn.do(o)
        logg.debug('faucet deployed with hash {}'.format(r))

        o = receipt(r)
        r = self.conn.do(o)
        self.address = to_checksum_address(r['contract_address'])
        logg.debug('faucet contract {}'.format(self.address))


    def test_basic(self):
        pass


if __name__ == '__main__':
    unittest.main()
