import base64 as b64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES

class AESCipher(object):

    def __init__(self, key): 
        self.bs = AES.block_size
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw):
        raw = b64.b64encode(raw.encode('utf-8')).decode('utf-8')
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return b64.b64encode(iv + cipher.encrypt(raw.encode()))

    def decrypt(self, enc, base64=True):
        enc = b64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        dec = self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')
        if base64:
            return b64.b64decode(dec).decode('utf-8')
        else:
            return dec

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]
