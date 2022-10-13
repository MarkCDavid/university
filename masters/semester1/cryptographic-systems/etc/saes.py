import numpy as np
from typing import List, Tuple
from bitarray2 import BitArray2

substitution_box = [
    [BitArray2.fromBitString("1001"),
    BitArray2.fromBitString("0100"),
    BitArray2.fromBitString("1010"),
    BitArray2.fromBitString("1011")],
    [BitArray2.fromBitString("1101"),
    BitArray2.fromBitString("0001"),
    BitArray2.fromBitString("1000"),
    BitArray2.fromBitString("0101")],
    [BitArray2.fromBitString("0110"),
    BitArray2.fromBitString("0010"),
    BitArray2.fromBitString("0000"),
    BitArray2.fromBitString("0011")],
    [BitArray2.fromBitString("1100"),
    BitArray2.fromBitString("1110"),
    BitArray2.fromBitString("1111"),
    BitArray2.fromBitString("0111")]
]

round_constants = [
    BitArray2.fromBitString("1000"),
    BitArray2.fromBitString("0000"),
    BitArray2.fromBitString("0011"),
    BitArray2.fromBitString("0000")
]

def to_nibbles(bitArray: 'BitArray2') -> 'List[BitArray2]':
    
    return [
        bitArray[0:4],
        bitArray[8:12],
        bitArray[4:8],
        bitArray[12:16]
    ]

def to_snibbles(bitArray: 'BitArray2') -> 'List[BitArray2]':
    return [
        bitArray[0:4],
        bitArray[4:8],
        bitArray[8:12],
        bitArray[12:16]
    ]

def from_nibbles(nibbles: 'List[BitArray2]') -> 'BitArray2':
    return sum(nibbles, start=BitArray2.empty(0))

def from_snibbles(nibbles: 'List[BitArray2]') -> 'BitArray2':
    return nibbles[0] + nibbles[2] + nibbles[1] + nibbles[3]

def row_col(nibble: 'BitArray2') -> 'Tuple[int, int]':
    return 2 * nibble[0] + nibble[1], 2 * nibble[2] + nibble[3]

def sbox(nibble: 'BitArray2') -> 'BitArray2':
    row, col = row_col(nibble)
    return substitution_box[row][col]

def subkeys_g(word: 'BitArray2', iteration: 'int'):
    n0, n1 = word[:4], word[4:]
    n0, n1 = sbox(n1), sbox(n0)
    n0, n1 = n0 ^ round_constants[iteration * 2 + 0], n1 ^ round_constants[iteration * 2 + 1]
    return n0 + n1

def resize(array, size):
    _z = min(len(array), size)
    result = np.zeros(size)
    result[size - _z:size] = array[0: _z]
    return result

def polynomial_multiplication_modulo(
    left: 'BitArray2', 
    right: 'BitArray2', 
    modulo: 'BitArray2') -> 'BitArray2':
    _, remainder = np.polydiv(np.polymul(left.toNumPyArray(), right.toNumPyArray()), modulo.toNumPyArray())
    return np.mod(resize(remainder, 4), 2)

def column_polynomial_multiplication_modulo(
    left: 'Tuple[BitArray2, BitArray2]', 
    right: 'Tuple[BitArray2, BitArray2]', 
    modulo: 'BitArray2') -> 'BitArray2':
    
    pmm0 = polynomial_multiplication_modulo(left[0], right[0], modulo)
    pmm1 = polynomial_multiplication_modulo(left[1], right[1], modulo)
    return np.mod(pmm0 + pmm1, 2)

    

def mixcol(nibbles: 'List[BitArray2]') -> 'List[BitArray2]':

    mip = BitArray2.fromBitString("10011")
    mcc_top = (BitArray2.fromBitString("1"), BitArray2.fromBitString("100"))
    mcc_bot = (BitArray2.fromBitString("100"), BitArray2.fromBitString("1"))
    
    col1 = (nibbles[0], nibbles[2])
    col2 = (nibbles[1], nibbles[3])

    mcol1 = (
        BitArray2.fromNumPyArray(column_polynomial_multiplication_modulo(mcc_top, col1, mip)),
        BitArray2.fromNumPyArray(column_polynomial_multiplication_modulo(mcc_bot, col1, mip))
    )

    mcol2 = (
        BitArray2.fromNumPyArray(column_polynomial_multiplication_modulo(mcc_top, col2, mip)),
        BitArray2.fromNumPyArray(column_polynomial_multiplication_modulo(mcc_bot, col2, mip))
    )

    return [mcol1[0], mcol2[0], mcol1[1], mcol2[1]]

def subkeys(key: 'BitArray2'):
    nibbles = to_nibbles(key)
    words = {}
    words[0] = nibbles[0] + nibbles[2]
    words[1] = nibbles[1] + nibbles[3]
    words[2] = words[0] ^ subkeys_g(words[1], 0)
    words[3] = words[1] ^ words[2]
    words[4] = words[2] ^ subkeys_g(words[3], 1)
    words[5] = words[3] ^ words[4]

    return [
        words[0] + words[1], 
        words[2][:4] + words[3][:4] + words[2][4:] + words[3][4:],
        words[4][:4] + words[5][:4] + words[4][4:] + words[5][4:]]

def encrypt(plaintext: 'BitArray2', key: 'BitArray2') -> 'BitArray2':
    _subkeys = subkeys(key)
    plaintext ^= _subkeys[0]
    nibbles = to_nibbles(plaintext)
    nibbles[0] = sbox(nibbles[0])
    nibbles[1] = sbox(nibbles[1])
    nibbles[2] = sbox(nibbles[2])
    nibbles[3] = sbox(nibbles[3])
    nibbles[2], nibbles[3] = nibbles[3], nibbles[2]
    nibbles = mixcol(nibbles)
    ciphertext = from_nibbles(nibbles)
    ciphertext ^= _subkeys[1]
    nibbles = to_snibbles(ciphertext)
    nibbles[0] = sbox(nibbles[0])
    nibbles[1] = sbox(nibbles[1])
    nibbles[2] = sbox(nibbles[2])
    nibbles[3] = sbox(nibbles[3])
    nibbles[2], nibbles[3] = nibbles[3], nibbles[2]
    ciphertext = from_nibbles(nibbles)
    ciphertext ^= _subkeys[2]
    return from_snibbles(to_snibbles(ciphertext))


if __name__ == "__main__":

    from saes_other import encryption

    result = encryption("0110111101101011", "1010011100111011")

    print(result)

    plaintext = BitArray2.fromBitString("0110111101101011")
    key = BitArray2.fromBitString("1010011100111011")

    result = encrypt(plaintext, key)
    print(result)
