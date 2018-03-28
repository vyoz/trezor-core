from common import *

from apps.nem.transaction import *
from trezor.crypto import hashlib


class TestNemTransactionProvisition(unittest.TestCase):

    def test_create_provision_namespace(self):

        # http://bob.nem.ninja:8765/#/transfer/0acbf8df91e6a65dc56c56c43d65f31ff2a6a48d06fc66e78c7f3436faf3e74f
        t = nem_transaction_create_provision_namespace(NEM_NETWORK_TESTNET,
                                                       56999445,
                                                       unhexlify('84afa1bbc993b7f5536344914dde86141e61f8cbecaf8c9cefc07391f3287cf5'),
                                                       20000000,
                                                       57003045,
                                                       'gimre',
                                                       '',
                                                       'TAMESPACEWH4MKFMBCVFERDPOOP4FK7MTDJEYP35',
                                                       5000000000)
        self.assertEqual(hashlib.sha3_256(t).digest(True), unhexlify('f7cab28da57204d01a907c697836577a4ae755e6c9bac60dcc318494a22debb3'))

        # http://bob.nem.ninja:8765/#/namespace/7ddd5fe607e1bfb5606e0ac576024c318c8300d237273117d4db32a60c49524d
        t = nem_transaction_create_provision_namespace(NEM_NETWORK_TESTNET,
                                                       21496797,
                                                       unhexlify('244fa194e2509ac0d2fbc18779c2618d8c2ebb61c16a3bcbebcf448c661ba8dc'),
                                                       108000000,
                                                       21500397,
                                                       'misc',
                                                       'alice',
                                                       'TAMESPACEWH4MKFMBCVFERDPOOP4FK7MTDJEYP35',
                                                       5000000000)
        self.assertEqual(hashlib.sha3_256(t).digest(True), unhexlify('7ddd5fe607e1bfb5606e0ac576024c318c8300d237273117d4db32a60c49524d'))

        # http://chain.nem.ninja/#/namespace/57071aad93ca125dc231dc02c07ad8610cd243d35068f9b36a7d231383907569
        t = nem_transaction_create_provision_namespace(NEM_NETWORK_MAINNET,
                                                       26699717,
                                                       unhexlify('9f3c14f304309c8b72b2821339c4428793b1518bea72d58dd01f19d523518614'),
                                                       108000000,
                                                       26703317,
                                                       'sex',
                                                       '',
                                                       'NAMESPACEWH4MKFMBCVFERDPOOP4FK7MTBXDPZZA',
                                                       50000000000)
        self.assertEqual(hashlib.sha3_256(t).digest(True), unhexlify('57071aad93ca125dc231dc02c07ad8610cd243d35068f9b36a7d231383907569'))


if __name__ == '__main__':
    unittest.main()
