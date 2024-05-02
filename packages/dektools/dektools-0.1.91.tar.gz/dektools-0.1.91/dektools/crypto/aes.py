from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


class CryptoBase:
    KEY = None
    IV = None

    encoding_key = 'utf-8'
    encoding_iv = 'utf-8'
    style = 'pkcs7'

    @property
    def cipher(self):
        return AES.new(self.KEY.encode(self.encoding_key), mode=AES.MODE_CBC, iv=self.IV.encode(self.encoding_iv))

    def _encrypt(self, bs):
        bs = pad(bs, AES.block_size, self.style)
        bs = self.cipher.encrypt(bs)
        return bs

    def _decrypt(self, bs):
        bs = self.cipher.decrypt(bs)
        bs = unpad(bs, AES.block_size, self.style)
        return bs
