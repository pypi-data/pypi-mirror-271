class SparrowBeDecryptionContentError(Exception):
    def __init__(self, error_message: str = None):
        if error_message is not None:
            self.error_message = error_message
        else:
            self.error_message = "输入的被解密数据不正确"

    def __str__(self):
        return self.error_message


class SparrowSecretKeyOverdueError(Exception):
    def __init__(self, error_message: str = None):
        if error_message is not None:
            self.error_message = error_message
        else:
            self.error_message = "秘钥已过期"

    def __str__(self):
        return self.error_message


class SparrowSecretKeyError(Exception):
    def __init__(self, error_message: str = None):
        if error_message is not None:
            self.error_message = error_message
        else:
            self.error_message = "秘钥错误"

    def __str__(self):
        return self.error_message


class SparrowDecompressionTypeError(Exception):
    def __init__(self, error_message: str = None):
        if error_message is not None:
            self.error_message = error_message
        else:
            self.error_message = "被解密数据类型错误，输入类型为字符串"

    def __str__(self):
        return self.error_message


class SparrowKeyTypeError(Exception):
    def __init__(self, error_message: str = None):
        if error_message is not None:
            self.error_message = error_message
        else:
            self.error_message = "秘钥类型错误，输入类型为字符串"

    def __str__(self):
        return self.error_message


class SparrowStringTypeError(Exception):
    def __init__(self, error_message: str = None):
        if error_message is not None:
            self.error_message = error_message
        else:
            self.error_message = "加密数据类型错误，输入类型为字符串"

    def __str__(self):
        return self.error_message


class SparrowCompressionRangeError(Exception):
    def __init__(self, error_message: str = None):
        if error_message is not None:
            self.error_message = error_message
        else:
            self.error_message = "范围错误，输入范围为[0, 1, 2]"

    def __str__(self):
        return self.error_message


class SparrowModeRangeError(Exception):
    def __init__(self, error_message: str = None):
        if error_message is not None:
            self.error_message = error_message
        else:
            self.error_message = "范围错误，输入范围为[0, 1]"

    def __str__(self):
        return self.error_message



