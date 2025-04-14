# ciphers.py

from Crypto.Cipher import AES 
import os 
import numpy as np

BLOCK_SIZE = 16
AES_KEY = os.urandom(16)
IV = os.urandom(16)
NONCE = os.urandom(8)

class CipherMode:
    def __init__(self, key=AES_KEY):
        self.key = key
    
    def encrypt(self, plaintext: bytes) -> bytes:
        raise NotImplementedError
    
    def decrypt (self, ciphertext: bytes) -> bytes:
        raise NotImplementedError
    
class ECBMode(CipherMode):
    def encrypt(self, plaintext: bytes) -> bytes:
        cipher = AES.new(self.key, AES.MODE_ECB)
        return cipher.encrypt(plaintext)
    
    def decrypt(self, ciphertext: bytes) -> bytes:
        cipher = AES.new(self.key, AES.MODE_ECB)
        return cipher.decrypt(ciphertext)
    
class CBCMode(CipherMode):
    def encrypt(self, plaintext: bytes) -> bytes:
        cipher = AES.new(self.key, AES.MODE_CBC, iv=IV)
        return cipher.encrypt(plaintext)
    
    def decrypt(self, ciphertext:bytes) -> bytes:
        cipher = AES.new(self.key, AES.MODE_CBC, iv=IV)
        return cipher.decrypt(ciphertext)
    
class CTRMode(CipherMode):
    def encrypt(self, plaintext: bytes) -> bytes:
        cipher = AES.new(self.key, AES.MODE_CTR, nonce=NONCE)
        return cipher.encrypt(plaintext)
    
    def decrypt(self, ciphertext: bytes) -> bytes:
        cipher = AES.new(self.key, AES.MODE_CTR, nonce=NONCE)
        return cipher.decrypt(ciphertext)
    
class ManualCBC(CipherMode):
    def __init__(self, key=AES_KEY, iv=IV):
        super().__init__(key)
        self.iv = iv
        self.ecb = AES.new(self.key, AES.MODE_ECB)

    def _pad(self, data: bytes) -> bytes:
        padding_length = BLOCK_SIZE - (len(data) % BLOCK_SIZE)
        return data + bytes([padding_length] * padding_length)

    def _unpad(self, data: bytes) -> bytes:
        padding_length = data[-1]
        return data[:-padding_length]

    def encrypt(self, plaintext: bytes) -> bytes:
        plaintext = self._pad(plaintext)
        # ciphertext = b""
        ciphertext_blocks = []
        # previous = self.iv
        previous = np.frombuffer(self.iv, dtype=np.uint8)

        for i in range(0, len(plaintext), BLOCK_SIZE):
            block = plaintext[i:i+BLOCK_SIZE]
            block_array = np.frombuffer(block, dtype=np.uint8)
            # xored = bytes(a^b for a, b in zip(block, previous))
            xored = np.bitwise_xor(block_array, previous)
            # encrypted = self.ecb.encrypt(xored)
            encrypted = self.ecb.encrypt(xored.tobytes())
            # ciphertext += encrypted
            ciphertext_blocks.append(encrypted)
            # previous = encrypted
            previous = np.frombuffer(encrypted, dtype=np.uint8)
        # return ciphertext
        return b''.join(ciphertext_blocks)
    
    def decrypt(self, ciphertext: bytes) -> bytes:
        # plaintext = b""
        plaintext_blocks = []
        # previous = self.iv
        previous = np.frombuffer(self.iv, dtype=np.uint8)

        for i in range(0, len(ciphertext), BLOCK_SIZE):
            block = ciphertext[i:i+BLOCK_SIZE]
            decrypted = self.ecb.decrypt(block)
            decrypted_array = np.frombuffer(decrypted, dtype=np.uint8)
            # xored = bytes(a^b for a, b in zip(decrypted, previous))
            xored = np.bitwise_xor(decrypted_array, previous)
            plaintext_blocks.append(xored.tobytes())
            # plaintext += xored
            # previous = block
            previous = np.frombuffer(block, dtype=np.uint8)
        # return self._unpad(plaintext)
        plaintext = b''.join(plaintext_blocks)
        return self._unpad(plaintext)

        
