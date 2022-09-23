from typing import List
from etc.bitarray import BitArray
from etc.DES.deshelper import P56, P48, IP, IP_reverse, Expansion, Straight, S0, S1, S2, S3, S4, S5, S6, S7, from_blocks, to_blocks

def _subkey(key: 'BitArray', shift: 'int') -> 'BitArray':
    key = P56(key)
    left, right = key.left() << shift, key.right() << shift
    return P48(left + right) 

def _subkeys(key: 'BitArray') -> 'List[BitArray]':
    return [_subkey(key, shift) for shift in [1, 2, 4, 6, 8, 10, 12, 14, 15, 17, 19, 21, 23, 25, 27, 28]]

def _f(bits: 'BitArray', subkey: 'BitArray') -> 'BitArray':
    bits = Expansion(bits) ^ subkey
    s0, s1, s2, s3, s4, s5, s6, s7 = bits.split(8)
    bits = S0(s0) + S1(s1) + S2(s2) + S3(s3) + S4(s4) + S5(s5) + S6(s6) + S7(s7)
    return Straight(bits)

def _round(bits: 'BitArray', subkey: 'BitArray') -> 'BitArray':
    left, right = bits.split()
    return right + (left ^ _f(right, subkey))

def _des(block: 'BitArray', subkeys: 'List[BitArray]') -> 'BitArray':
    block = IP(block)
    for subkey in subkeys:
        block = _round(block, subkey)
    return IP_reverse(block.swap_halves()) # last round performs unneccessary swap, as such, we have to unswap

def _des_blocks(bits: 'BitArray', subkeys: 'List[BitArray]') -> 'BitArray':
    return from_blocks(_des(block, subkeys) for block in to_blocks(bits))

def encrypt(plaintext: 'BitArray', key: 'BitArray') -> 'BitArray':
    subkeys = _subkeys(key)
    return _des_blocks(plaintext, subkeys)

def decrypt(ciphertext: 'BitArray', key: 'BitArray') -> 'BitArray':
    subkeys = list(reversed(_subkeys(key)))
    return _des_blocks(ciphertext, subkeys)

