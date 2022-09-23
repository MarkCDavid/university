from typing import Tuple
from etc.caesar import CaesarCipher

class VigenereCipher:

    def __init__(self, *, alphabet: 'str', key: 'str') -> None:
        self.cipher = [
            CaesarCipher(alphabet=alphabet, offset=alphabet.index(symbol))
            for symbol
            in key
        ]

    def compute(self: 'VigenereCipher', text: 'str') -> 'str':
        return ''.join(
            self.cipher[index % len(self.cipher)].compute(symbol)
            for index, symbol
            in enumerate(text)
        )

# A pair of Vigenere Ciphers, one used for encrpytion, one used for decrpytion.
def encrypt_decrypt_pair(*, alphabet: 'str',  key: 'str') -> 'Tuple[VigenereCipher, VigenereCipher]':
    decryption_key = ''.join(
        alphabet[-alphabet.index(symbol)] 
        for symbol 
        in key)

    return (
        VigenereCipher(alphabet=alphabet, key=key), 
        VigenereCipher(alphabet=alphabet, key=decryption_key)
    )

if __name__ == '__main__':
    from string import ascii_uppercase as alphabet
   
    key = "VILNIUS"

    print("Vigenere Cipher:")
    print("Alphabet:", alphabet)
    print("     Key:", key)

    encrypt, decrypt = encrypt_decrypt_pair(alphabet=alphabet, key=key)

    plaintext = "VILNIUSGEDIMINASTECHNICALUNIVERSITY"
    print("          Plaintext:", plaintext)

    ciphertext = encrypt.compute(plaintext)
    print("         Ciphertext:", ciphertext)
    decrypted_plaintext = decrypt.compute(ciphertext)
    print("Decrypted Plaintext:", decrypted_plaintext)
