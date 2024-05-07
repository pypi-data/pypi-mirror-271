import time
from sparrowEncryptionDecryption.function.config import KEYS1, KEYS2
from sparrowEncryptionDecryption.tools import binary_to_string
from sparrowEncryptionDecryption.tools import quaternary_to_binary
from sparrowEncryptionDecryption.tools import compression_and_decompression2
from sparrowEncryptionDecryption.tools import compression_and_decompression
from sparrowEncryptionDecryption.tools import SparrowBeDecryptionContentError
from sparrowEncryptionDecryption.tools import SparrowSecretKeyOverdueError
from sparrowEncryptionDecryption.tools import SparrowSecretKeyError
from sparrowEncryptionDecryption.tools import SparrowDecompressionTypeError
from sparrowEncryptionDecryption.tools import SparrowKeyTypeError


class SparrowDecryption(object):
    def __init__(self, keys1: dict = None, keys2: dict = None, try_mode: bool = False):
        self.try_mode = try_mode
        if keys1 is None:
            self.keys1 = KEYS1
        else:
            self.keys1 = keys1
        if keys2 is None:
            self.keys2 = KEYS2
        else:
            self.keys2 = keys2

    def order_decryption(self, decompression: str, key: str):
        """
        将被加密的数据解密
        :param decompression: 需要被解密的数据
        :param key: 秘钥
        :return: 返回被解密的数据或秘钥错误类型
        """
        if type(decompression) is not str:
            if self.try_mode:
                raise SparrowDecompressionTypeError
        if type(key) is not str:
            if self.try_mode:
                raise SparrowKeyTypeError
        string = None
        if "三" in decompression:
            try:
                if "零" in decompression:
                    decompression = decompression.replace("零", '').replace("三", "")
                else:
                    if "一" in decompression:
                        decompression = compression_and_decompression(False, decompression.replace("一", '').replace("三", ""), self.keys1)
                    elif "二" in decompression:
                        decompression = compression_and_decompression(False, compression_and_decompression2(False, decompression.replace("二", "").replace( "三", ""), self.keys2) + "", self.keys1)
                    else:
                        if self.try_mode:
                            raise SparrowBeDecryptionContentError
                string = binary_to_string(
                    decompression.replace("A", "00").replace("T", "01").replace("C", "11").replace("G", "10")).split(";")
            except Exception:
                if self.try_mode:
                    raise SparrowBeDecryptionContentError
        elif "四" in decompression:
            try:
                if "零" in decompression:
                    decompression = decompression.replace("零", '').replace("四", "")
                else:
                    if "一" in decompression:
                        decompression = compression_and_decompression(False, decompression.replace("一", '').replace("四", ""), self.keys1)
                    elif "二" in decompression:
                        decompression = compression_and_decompression(False, compression_and_decompression2(False, decompression.replace("二", "").replace("四", ""), self.keys2), self.keys1)
                    else:
                        if self.try_mode:
                            raise SparrowBeDecryptionContentError
                binary = quaternary_to_binary(
                    decompression.replace("A", "0").replace("T", "1").replace("C", "2").replace("G", "3"))
                string = binary_to_string(binary).split(';')
            except Exception:
                if self.try_mode:
                    raise SparrowBeDecryptionContentError
        else:
            if self.try_mode:
                if self.try_mode:
                    raise SparrowBeDecryptionContentError
        if string[1] != "-1":
            effective_duration = int(time.time() - float(string[3]))
            if string[2] == key:
                if effective_duration < int(string[1]):
                    return string[0]
                else:
                    if self.try_mode:
                        raise SparrowSecretKeyOverdueError
            else:
                if self.try_mode:
                    raise SparrowSecretKeyError
        else:
            if string[2] == key:
                return string[0]
            else:
                if self.try_mode:
                    raise SparrowSecretKeyError

