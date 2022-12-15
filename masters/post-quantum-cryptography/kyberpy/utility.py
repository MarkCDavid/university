from typing import List
from bitarray import BitArray

def to_unsigned_byte(value: 'int') -> 'int':
    return value & 0xFF

def to_signed_byte(value: 'int') -> 'int':
    value = to_unsigned_byte(value)
    return value if value < 2**7 else value - 2**8

def to_unsigned_short(value: 'int') -> 'int':
    return value & 0xFFFF

def to_signed_short(value: 'int') -> 'int':
    value = to_unsigned_short(value)
    return value if value < 2**15 else value - 2**16

def reduce(polynomial: 'List[int]', modulo: 'int') -> 'List[int]':
    return [coefficient % modulo for coefficient in polynomial]

class Nonce:
    def __init__(self: 'Nonce', value: 'int' = 0) -> 'None':
        self.value = to_signed_byte(value)

    def next(self: 'Nonce') -> 'int':
        nonce = self.value
        self.value = to_signed_byte(self.value + 1)
        return nonce


class BitStream:
    def __init__(self: 'BitStream', bits: 'BitArray') -> 'None':
        self.index = 0
        self.bits = bits

    def can_read(self: 'BitStream', count: 'int') -> 'bool':
        return self.index + count < len(self.bits)

    def read(self: 'BitStream', count: 'int') -> 'BitArray':
        result = self.bits.slice(self.index, count)
        self.index += count
        return result