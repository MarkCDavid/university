from typing import Tuple, Union
from math import ceil

class BitArray:

    def __init__(self, size: 'int', bits: 'int') -> 'None':
        self.size = size
        self.bits = bits

    @staticmethod
    def fromString(string: 'str', encoding: 'str') -> 'BitArray':
        bytes = string.encode(encoding)
        return BitArray(len(bytes) * 8, int.from_bytes(bytes, "little"))

    @staticmethod
    def fromBitString(string: 'str') -> 'BitArray':
        assert all(symbol == '0' or symbol == '1' for symbol in string)
        values = [int(symbol) for symbol in string]

        result = BitArray.empty(len(string))
        for index, value in enumerate(values):
            result[index] = value
                
        return result 

    @staticmethod
    def fromBitArray(bitArray: 'BitArray') -> 'BitArray':
        return BitArray(bitArray.size, bitArray.bits)

    @staticmethod
    def empty(size: 'int') -> 'BitArray':
        return BitArray(size, 0)

    def split(self) -> 'Tuple[BitArray, BitArray]':
        return self.left(), self.right()

    def left(self) -> 'BitArray':
        middle = ceil(len(self) / 2)
        return self[:middle]

    def right(self) -> 'BitArray':
        middle = ceil(len(self) / 2)
        return self[middle:]

    def __eq__(self: 'BitArray', other: 'BitArray') -> 'bool':
        return self.bits == other.bits

    def __add__(self: 'BitArray', other: 'BitArray') -> 'BitArray':
        result = BitArray.empty(self.size + other.size)
        for sourceIndex, targetIndex in enumerate(range(self.size)):
            result[targetIndex] = self[sourceIndex]

        for sourceIndex, targetIndex in enumerate(range(self.size, self.size + other.size)):
            result[targetIndex] = other[sourceIndex]
        
        return result

    def __xor__(self: 'BitArray', other: 'BitArray') -> 'BitArray':
        size = min(self.size, other.size)
        result = BitArray.empty(size)

        for index in range(size):
            result[index] = self[index] ^ other[index]
        
        return result

    def __lshift__(self: 'BitArray', amount: 'int') -> 'BitArray':
        return self._circular_shift(-amount)

    def __rshift__(self: 'BitArray', amount: 'int') -> 'BitArray':
        return self._circular_shift(amount)

    def _circular_shift(self: 'BitArray', amount: 'int') -> 'BitArray':
        if self.size == 0:
            return BitArray.empty(0)

        result = BitArray.fromBitArray(self)
        
        for source in range(result.size):
            target = (source + amount) % result.size
            result[target] = self[source]

        return result
   
    def __setitem__(self, index: 'int', value: 'int') -> 'None':
        self._assert_index_within_range(index)
        self._assert_value_within_range(value)
        self._set(index) if value else self._unset(index)

    def __getitem__(self, coordinate: 'Union[int, slice]') -> 'int':
        if isinstance(coordinate, int):
            return self.__getitem_index__(coordinate)

        if isinstance(coordinate, slice):
            return self.__getitem_slice__(coordinate)
        
        raise Exception()

    def __getitem_index__(self, index: 'int') -> 'int':
        assert index < self.size
        return (self.bits >> index) & 1

    def __getitem_slice__(self: 'BitArray', slice: 'slice') -> 'BitArray':
        start, stop, step = self._unpack_silce(slice)
        bit_count = ceil((stop - start) / step)

        result = BitArray(bit_count, 0)
        for targetIndex, sourceIndex in enumerate(range(start, stop, step)):
            result[targetIndex] = self[sourceIndex]
        
        return result

    def _set(self, index) -> None:
        self.bits |= (1 << index)

    def _unset(self, index) -> None:
        self.bits &= (~(1 << index))

    def _unpack_silce(self, slice: 'slice') -> 'Tuple[int, int, int]':
        start, stop, step = slice.start or 0, slice.stop or self.size, slice.step or 1
        self._assert_index_within_range(start)
        self._assert_index_within_range(stop)
        start, stop = (stop, start - 1) if step < 0 else (start, stop)
        return start, stop, step

    def _assert_index_within_range(self, index: 'int'):
        assert index >= 0 and index <= self.size

    def _assert_value_within_range(self, value: 'int'):
        assert value == 0 or value == 1
    
    def __str__(self) -> 'str':
        return ''.join(str(self[index]) for index in range(self.size))

    def __len__(self) -> 'int':
        return self.size
