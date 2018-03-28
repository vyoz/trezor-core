from common import *

from apps.nem.transaction import *
from trezor.crypto import hashlib


class TestNemTransactionMosaicCreation(unittest.TestCase):

    def test_nem_transaction_create_mosaic_supply_change(self):

        # http://bigalice2.nem.ninja:7890/transaction/get?hash=33a50fdd4a54913643a580b2af08b9a5b51b7cee922bde380e84c573a7969c50
        t = nem_transaction_create_mosaic_supply_change(NEM_NETWORK_TESTNET,
                                                        14071648,
                                                        unhexlify("994793ba1c789fa9bdea918afc9b06e2d0309beb1081ac5b6952991e4defd324"),
                                                        108000000,
                                                        14075248,
                                                        "gimre.games.pong",
                                                        "paddles",
                                                        1,
                                                        1234)

        self.assertEqual(hashlib.sha3_256(t).digest(True),
                         unhexlify('33a50fdd4a54913643a580b2af08b9a5b51b7cee922bde380e84c573a7969c50'))

        # http://bigalice2.nem.ninja:7890/transaction/get?hash=1ce8e8894d077a66ff22294b000825d090a60742ec407efd80eb8b19657704f2
        t = nem_transaction_create_mosaic_supply_change(NEM_NETWORK_TESTNET,
                                                        14126909,
                                                        unhexlify("84afa1bbc993b7f5536344914dde86141e61f8cbecaf8c9cefc07391f3287cf5"),
                                                        108000000,
                                                        14130509,
                                                        "jabo38_ltd.fuzzy_kittens_cafe",
                                                        "coupons",
                                                        2,
                                                        1)

        self.assertEqual(hashlib.sha3_256(t).digest(True),
                         unhexlify('1ce8e8894d077a66ff22294b000825d090a60742ec407efd80eb8b19657704f2'))

        # http://bigalice3.nem.ninja:7890/transaction/get?hash=694e493e9576d2bcf60d85747e302ac2e1cc27783187947180d4275a713ff1ff
        t = nem_transaction_create_mosaic_supply_change(NEM_NETWORK_MAINNET,
                                                        53377685,
                                                        unhexlify("b7ccc27b21ba6cf5c699a8dc86ba6ba98950442597ff9fa30e0abe0f5f4dd05d"),
                                                        20000000,
                                                        53464085,
                                                        "abvapp",
                                                        "abv",
                                                        1,
                                                        9000000)

        self.assertEqual(hashlib.sha3_256(t).digest(True),
                         unhexlify('694e493e9576d2bcf60d85747e302ac2e1cc27783187947180d4275a713ff1ff'))

        # http://bigalice3.nem.ninja:7890/transaction/get?hash=09836334e123970e068d5b411e4d1df54a3ead10acf1ad5935a2cdd9f9680185
        t = nem_transaction_create_mosaic_supply_change(NEM_NETWORK_MAINNET,
                                                        55176304,
                                                        unhexlify("75f001a8641e2ce5c4386883dda561399ed346177411b492a677b73899502f13"),
                                                        20000000,
                                                        55262704,
                                                        "sushi",
                                                        "wasabi",
                                                        2,
                                                        20)

        self.assertEqual(hashlib.sha3_256(t).digest(True),
                         unhexlify('09836334e123970e068d5b411e4d1df54a3ead10acf1ad5935a2cdd9f9680185'))


if __name__ == '__main__':
    unittest.main()
