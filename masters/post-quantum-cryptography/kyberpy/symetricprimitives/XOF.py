from typing import List
from utility import to_unsigned_byte
from bitarray import BitArray
from Crypto.Hash import SHAKE128

# REFERENCE: CRYSTALS-Kyber, Symmetric primitives, p. 5
# URL: https://pq-crystals.org/kyber/data/kyber-specification-round3-20210804.pdf

# eXtendable Output Function (XOF)
# input: bytearray, byte, byte
# output: bytearray

# XOF initialised using SHAKE128
def XOF(seed: 'List[int]', i: 'int', j: 'int') -> 'BitArray':
    shake128 = SHAKE128.new()
    shake128.update(bytearray(to_unsigned_byte(x) for x in seed))
    shake128.update(bytearray([i, j]))
    return BitArray.fromBytes(bytes(to_unsigned_byte(byte) for byte in shake128.read(672)))