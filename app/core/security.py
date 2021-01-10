from passlib.context import CryptContext
from Crypto.Cipher import AES
from enum import unique, Enum

@unique
class Mode(Enum):
    CBC = AES.MODE_CBC
    ECB = AES.MODE_ECB


@unique
class Padding(Enum):
    """ 定义填充的字符串 """
    SPACE = ' '  # 空格


class AES256Crypto:
    def __init__(self, key, mode=Mode.CBC, padding=Padding.SPACE, iv=None):
        """
        :param key: 密钥， 32byte 长度字符串
        :param mode: 加密模式， 来源 class Mode
        :param iv: 16byte 长度字符串
        :param padding: 填充的字符串， 来源class Padding
        """
        self.padding = self.check_padding(padding)

        self.key = self.padding_key(key)
        self.iv = self.padding_iv(iv) if iv else None

        self.mode = self.check_mode(mode)

    def check_mode(self, mode):
        """ 核对 mode """
        if mode not in Mode.__members__.values():
            raise Exception(f'mode {mode} not allowed!')
        if mode == Mode.CBC and not self.iv:
            raise Exception(f'iv is required')
        return mode

    def check_padding(self, padding):
        """ 核对 padding """
        if padding not in Padding.__members__.values():
            raise Exception(f'mode {padding} not allowed!')
        return padding

    def padding_ret_byte(self, text, _len=16):
        """ 填充并转成 bytes """
        text = text.encode()
        remainder = len(text) % _len
        remainder = _len if remainder == 0 else remainder
        text += (_len - remainder) * self.padding.value.encode()
        return text

    def padding_iv(self, iv: str):
        """ 补全iv 并转成 bytes"""
        if len(iv.encode()) > 16:
            raise Exception(f'iv {iv} must <= 16bytes')
        return self.padding_ret_byte(iv)

    def padding_key(self, key: str):
        """ 补全key 并转成 bytes """
        if len(key.encode()) > 32:
            raise Exception(f'key {key} must <= 32bytes')
        return self.padding_ret_byte(key, _len=32)

    def encrypt(self, text, encode=None):
        """
        加密
        :param text: 待加密字符串
        :param encode: 传入base64里面的方法
        :return:  若encode=None则不进行base加密处理，返回bytes类型数据
        """
        text = self.padding_ret_byte(text)
        # 注意：加密中的和解密中的AES.new()不能使用同一个对象，所以在两处都使用了AES.new()
        text = AES.new(key=self.key, mode=self.mode.value, iv=self.iv).encrypt(text)
        if encode:
            return encode(text).decode()
        return text

    def decrypt(self, text, decode=None):
        """ 解密 """
        if decode:
            if type(text) == str:
                text = text.encode()
            text = decode(bytes(text))
        else:
            if type(text) != bytes:
                raise Exception(text)
        text = AES.new(key=self.key, mode=self.mode.value, iv=self.iv).decrypt(text)
        text = text.strip(self.padding.value.encode())
        return text.decode()


if __name__ == '__main__':
    import json

    # 这是一段待加密的字符串
    text = '{"upi": "1341343", "overdue": "2020-11-26 00:00:00"}'
    key = 't6LtKa3tD5X6qaJ6qOrAW3XmobFrY6ob'
    iv = 'NjtP47eSECuOm3s6'
    aes = AES256Crypto(key, Mode.CBC, Padding.SPACE, iv)
    text_1 = aes.encrypt(text)
    # b'\xe7\x1d\xeae\xff\xc7\xc2\xd7\x8c\xf6\xe7\x82u\x7f\x168\xbc\x90\xad\x1e\x85M\xcb\xb0\xb4Ho\x1b\xe4\xec\x9d\x1d\xf93\xeb\x9b\xe7\xa3\xdd$\x8cEa\xab\xf7K~\x91H\xc3]5\xc4\x1a\xd4w[\x83\xb2"FC\x9f\x9d'
    text_2 = aes.decrypt(text_1)
    # '{"upi": "1341343", "overdue": "2020-11-26 00:00:00"}'

    import base64

    text_3 = aes.encrypt(text, encode=base64.b16encode)
    # 'E71DEA65FFC7C2D78CF6E782757F1638BC90AD1E854DCBB0B4486F1BE4EC9D1DF933EB9BE7A3DD248C4561ABF74B7E9148C35D35C41AD4775B83B22246439F9D'
    text_4 = aes.decrypt(text_3, decode=base64.b16decode)
    # '{"upi": "1341343", "overdue": "2020-11-26 00:00:00"}'