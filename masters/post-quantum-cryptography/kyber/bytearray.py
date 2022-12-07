from itertools import chain
from typing import List, Union

class BitArray():
    def __init__(self: 'BitArray', bits: 'List[int]') -> None:
        BitArray._assert_within_range(bits)
        self.bits = bits

    def concat(self: 'BitArray', other: 'BitArray') -> 'BitArray':
        return BitArray(self.bits + other.bits)

    def __str__(self: 'BitArray') -> 'str':
        return ''.join(str(bit) for bit in self.bits)

    def __getitem__(self: 'BitArray', index: 'int') -> 'int':
        return self.bits[index % len(self.bits)]

    @staticmethod
    def _assert_within_range(bits: 'List[int]'):
        for bit in bits:
            assert bit == 0 or bit == 1

class ByteArray():
    def __init__(self: 'ByteArray', bytes: 'List[int]') -> None:
        ByteArray._assert_within_range(bytes)
        self.bytes = bytes

    def concat(self: 'ByteArray', other: 'ByteArray') -> 'ByteArray':
        return ByteArray(self.bytes + other.bytes)

    def part(self: 'ByteArray', at: 'int') -> 'ByteArray':
        assert at >= 0 and at <= len(self.bytes)
        return ByteArray(self.bytes[at:])

    def toBits(self: 'ByteArray') -> 'BitArray':
        return BitArray(list(chain.from_iterable(ByteArray._toBits(byte) for byte in self.bytes)))

    def __str__(self: 'ByteArray') -> 'str':
        return ' '.join(str(byte) for byte in self.bytes)

    def __getitem__(self: 'ByteArray', index: 'int') -> 'int':
        return self.bytes[index % len(self.bytes)]

    @staticmethod
    def _toBits(byte: 'int') -> 'List[int]':
        return [(byte >> i) & 1 for i in range(8)]

    @staticmethod
    def _assert_within_range(bytes: 'List[int]'):
        for byte in bytes:
            assert byte >= 0 and byte <= 255
