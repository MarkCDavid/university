from typing import List, Callable
from bitarray import BitArray
from sdeshelper import P10, P8, IP8, IP8_reverse, EP, P4, S0, S1, to_blocks, from_blocks

def _subkey(key: 'BitArray', shift: 'int') -> 'BitArray':
    key = P10(key)
    left, right = key.left() << shift, key.right() << shift
    return P8(left + right) 

def _subkeys(key: 'BitArray') -> 'List[BitArray]':
    return [_subkey(key, shift) for shift in [1, 3]]

def _f(bits: 'BitArray', subkey: 'BitArray') -> 'BitArray':
    bits = EP(bits) ^ subkey
    bits = S0(bits.left()) + S1(bits.right())
    return P4(bits)

def _round(bits: 'BitArray', subkey: 'BitArray') -> 'BitArray':
    left, right = bits.split()
    return right + (left ^ _f(right, subkey))

def _sdes(block: 'BitArray', subkeys: 'List[BitArray]') -> 'BitArray':
    block = IP8(block)
    for subkey in subkeys:
        block = _round(block, subkey)
    return IP8_reverse(block.swap_halves()) # last round performs unneccessary swap, as such, we have to unswap

def _sdes_blocks(bits: 'BitArray', subkeys: 'List[BitArray]') -> 'BitArray':
    return from_blocks(_sdes(block, subkeys) for block in to_blocks(bits))

def encrypt(plaintext: 'BitArray', key: 'BitArray') -> 'BitArray':
    subkeys = _subkeys(key)
    return _sdes_blocks(plaintext, subkeys)

def decrypt(ciphertext: 'BitArray', key: 'BitArray') -> 'BitArray':
    subkeys = list(reversed(_subkeys(key)))
    return _sdes_blocks(ciphertext, subkeys)

