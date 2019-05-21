from binascii import unhexlify

class Ripemd160():
    def __init__(self, d):
        self.data = d

    def __bytes__(self):
        return unhexlify(bytes(self.data, 'utf-8'))

    def __str__(self):
        return str(self.data)

