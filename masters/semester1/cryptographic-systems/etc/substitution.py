import random
from copy import copy
from typing import Tuple

class SubstitutionCipher:
    def __init__(self: 'SubstitutionCipher', *, alphabet: 'str', key: 'str'):
        assert len(alphabet) == len(key)
        self.alphabet = alphabet
        self.key = key

    def compute(self: 'SubstitutionCipher', text: 'str') -> 'str':
        return ''.join(
            self.key[self.alphabet.index(symbol)] 
            for symbol 
            in text)


# A pair of Substitution Ciphers, one used for encrpytion, one used for decrpytion.
def encrypt_decrypt_pair(*, alphabet: 'str',  key: 'str') -> 'Tuple[SubstitutionCipher, SubstitutionCipher]':
    return (
        SubstitutionCipher(alphabet=alphabet, key=key), 
        SubstitutionCipher(alphabet=key, key=alphabet)
    )

def shuffle(sequence: 'str') -> 'str':
    sequence = copy(list(sequence))
    random.shuffle(sequence)
    return ''.join(sequence)

if __name__ == '__main__':
    from string import ascii_uppercase
    alphabet = ascii_uppercase
    key = shuffle(alphabet)

    print("Substitution Cipher:")
    print("Alphabet:", alphabet)
    print("     Key:", key)

    encrypt, decrypt = encrypt_decrypt_pair(alphabet=alphabet, key=key)

    plaintext = "AURIMASSAKALYS"
    print("          Plaintext:", plaintext)

    ciphertext = encrypt.compute(plaintext)
    print("         Ciphertext:", ciphertext)
    decrypted_plaintext = decrypt.compute(ciphertext)
    print("Decrypted Plaintext:", decrypted_plaintext)
