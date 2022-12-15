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

    def str_max(self: 'BitArray', count: 'int') -> 'str':
        bits = self.bits
        result = ''
        for _ in range(count):
            result += str(bits & 1)
            bits = bits >> 1
        return result

    def __getitem__(self: 'BitArray', index: 'int') -> 'int':
        return self.bits >> index & 1

    # def __getitem__(self: 'BitArray', _slice: 'slice') -> 'BitArray':
    #     value = self.bits >> _slice.start
    #     mask = ~(n_1_bits(self.bits.bit_length()) << (_slice.stop - _slice.start))
    #     return BitArray(value & mask)

    def __and__(self: 'BitArray', mask: 'int') -> 'BitArray':
        return BitArray(self.bits & mask)