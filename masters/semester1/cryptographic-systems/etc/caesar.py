#!/usr/bin/python3
from typing import Dict, Tuple

def shift(string: 'str', amount: 'int') -> str:
    amount %= len(string)
    return string[amount:] + string[:amount]

class CaesarCipher:
    def __init__(self: 'CaesarCipher', *, alphabet: 'str', offset: 'int'):
        self.cipher: 'Dict[str, str]' = {
            source:target
            for (source, target)
            in zip(alphabet, shift(alphabet, offset))
        }

    def compute(self: 'CaesarCipher', text: 'str') -> 'str':
        return ''.join(
            # if we cannot find the symbol in the map, we simply use the original symbol
            self.cipher[symbol] if symbol in self.cipher else symbol
            for symbol 
            in text)

# A pair of Caesar Ciphers, one used for encrpytion, one used for decrpytion.
def encrypt_decrypt_pair(*, alphabet: 'str', offset: 'int') -> 'Tuple[CaesarCipher, CaesarCipher]':
    return (
        CaesarCipher(alphabet=alphabet, offset=offset), 
        CaesarCipher(alphabet=alphabet, offset=-offset)
    )


