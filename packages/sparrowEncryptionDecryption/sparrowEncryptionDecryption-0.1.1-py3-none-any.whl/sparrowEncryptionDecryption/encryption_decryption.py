from sparrowEncryptionDecryption.function.config import KEYS1, KEYS2
from sparrowEncryptionDecryption.function import SparrowDecryption, SparrowEncryption


class SparrowEncryptionDecryption(object):
    def __init__(self, keys1: dict = None, keys2: dict = None, try_mode: bool = False):
        if keys1 is None:
            self.keys1 = KEYS1
        else:
            self.keys1 = keys1
        if keys2 is None:
            self.keys2 = KEYS2
        else:
            self.keys2 = keys2
        self.encryption = SparrowEncryption(self.keys1, self.keys2, try_mode)
        self.decryption = SparrowDecryption(self.keys1, self.keys2, try_mode)

    def order_encryption(self, string: str, key: str, effective_duration=-1, is_compression=2, mode=0):
        return self.encryption.order_encryption(string, key, effective_duration, is_compression, mode)

    def order_decryption(self, decompression: str, key: str):
        return self.decryption.order_decryption(decompression, key)


