from typing import List
from kmath import n_1_bits

class BitArray:

    @staticmethod
    def fromBytes(_bytes: 'bytes') -> 'BitArray':
        return BitArray(int.from_bytes(_bytes, 'little'))

    def __init__(self: 'BitArray', bits: 'int'):
        self.bits = bits

    def __rshift__(self: 'BitArray', amount: 'int') -> 'BitArray':
        return BitArray(self.bits >> amount)

    def __str__(self: 'BitArray') -> 'str':
        bits = self.bits
        result = ''
        while bits > 0:
            result += str(bits & 1)
            bits = bits >> 1
        return result


    def __getitem__(self: 'BitArray', index: 'int') -> 'int':
        return self.bits >> index & 1

    def slice(self: 'BitArray', start: 'int', count: 'int') -> 'BitArray':
        value = self.bits >> start
        mask = ~(n_1_bits(self.bits.bit_length()) << count)
        return BitArray(value & mask)

    def slice_bytes(self: 'BitArray', start: 'int', count: 'int') -> 'BitArray':
        return self.slice(start * 8, count * 8)

    def __and__(self: 'BitArray', mask: 'int') -> 'BitArray':
        return BitArray(self.bits & mask)

    def __len__(self: 'BitArray') -> 'int':
        return self.bits.bit_length()