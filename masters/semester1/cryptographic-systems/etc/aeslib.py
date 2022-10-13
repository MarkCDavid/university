from etc.bitarray2 import BitArray2
from cryptography.hazmat.primitives.ciphers.algorithms import AES128
from cryptography.hazmat.primitives.ciphers.modes import CBC
from cryptography.hazmat.primitives.ciphers import Cipher
from cryptography.hazmat.primitives.padding import PKCS7
from cryptography.hazmat.backends import default_backend

def _pad(bitArray: 'BitArray2', size: 'int') -> 'BitArray2':
    padder = PKCS7(size).padder()
    padder.update(bitArray.toBytes())
    return BitArray2.fromBytes(padder.finalize())

def _unpad(bitArray: 'BitArray2', size: 'int') -> 'BitArray2':
    unpadder = PKCS7(size).unpadder()
    unpadder.update(bitArray.toBytes())
    return BitArray2.fromBytes(unpadder.finalize())

class AES:

    def __init__(self: 'AES', key: 'BitArray2') -> None:
        key = _pad(key, 128)
        self.cipher = Cipher(
            AES128(key.toBytes()),
            CBC(BitArray2.empty(128).toBytes()),
            default_backend()
        )

    def encrypt(self: 'AES', plaintext: 'BitArray2') -> 'BitArray2':
        plaintext = _pad(plaintext, 128)
        encryptor = self.cipher.encryptor()
        ciphertext = encryptor.update(plaintext.toBytes())
        return BitArray2.fromBytes(ciphertext)

    def decrypt(self: 'AES', ciphertext: 'BitArray2') -> 'BitArray2':
        decryptor = self.cipher.decryptor()
        plaintext = decryptor.update(ciphertext.toBytes())
        plaintext = _unpad(plaintext, 128)
        return BitArray2.fromBytes(plaintext)
    
