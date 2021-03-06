# Automatically generated by pb2py
import protobuf as p


class NEMDecryptMessage(p.MessageType):
    FIELDS = {
        1: ('address_n', p.UVarintType, p.FLAG_REPEATED),
        2: ('network', p.UVarintType, 0),
        3: ('public_key', p.BytesType, 0),
        4: ('payload', p.BytesType, 0),
    }
    MESSAGE_WIRE_TYPE = 75

    def __init__(
        self,
        address_n: list = None,
        network: int = None,
        public_key: bytes = None,
        payload: bytes = None,
        **kwargs,
    ):
        self.address_n = [] if address_n is None else address_n
        self.network = network
        self.public_key = public_key
        self.payload = payload
        p.MessageType.__init__(self, **kwargs)
