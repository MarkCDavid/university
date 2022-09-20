from typing import Tuple, Union
from math import ceil

class BitArray:

    def __init__(self, size: 'int', bits: 'int') -> 'None':
        self.size = size
        self.bits = bits

    @staticmethod
    def fromString(string: 'str', encoding: 'str') -> 'BitArray':
        _bytes = string.encode(encoding)
        bit_count = len(_bytes) * 8
        bits = int.from_bytes(_bytes, "little")
        return BitArray(bit_count, bits)

    @staticmethod
    def fromBitString(string: 'str') -> 'BitArray':
        assert all(symbol == '0' or symbol == '1' for symbol in string)
        values = [int(symbol) for symbol in string]

        result = BitArray.empty(len(string))
        for index, value in enumerate(values):
            result[index] = value
                
        return result 

    @staticmethod
    def empty(size: 'int') -> 'BitArray':
        return BitArray(size, 0)

    def split(self) -> 'Tuple[BitArray, BitArray]':
        return self.left(), self.right()

    def middle(self) -> 'int':
        return ceil(len(self) / 2)

    def left(self) -> 'BitArray':
        return self[:self.middle()]

    def right(self) -> 'BitArray':
        return self[self.middle():]

    def swap_halves(self) -> 'BitArray':
        left, right = self.split()
        return right + left

    def copy(self) -> 'BitArray':
        return BitArray(self.size, self.bits)

    def __len__(self) -> 'int':
        return self.size

    def __eq__(self: 'BitArray', other: 'BitArray') -> 'bool':
        return self.bits == other.bits

    def __add__(self: 'BitArray', other: 'BitArray') -> 'BitArray':
        return BitArray.fromBitString(str(self) + str(other))

    def __xor__(self: 'BitArray', other: 'BitArray') -> 'BitArray':
        return BitArray(min(self.size, other.size), self.bits ^ other.bits)

    def __lshift__(self: 'BitArray', amount: 'int') -> 'BitArray':
        return self._circular_shift(-amount)

    def __rshift__(self: 'BitArray', amount: 'int') -> 'BitArray':
        return self._circular_shift(amount)

    def __str__(self) -> 'str':
        return ''.join(str(bit) for bit in self)

    def __repr__(self) -> 'str':
        return f"BitArray.fromBitString({str(self)})"

    def __iter__(self) -> 'BitArray':
        return BitArrayIterator(self)
   
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
        self._assert_index_within_range(index)
        return (self.bits >> index) & 1

    def __getitem_slice__(self: 'BitArray', _slice: 'slice') -> 'BitArray':
        start, stop, step = self._unpack_silce(_slice)
        bit_count = ceil((stop - start) / step)

        result = BitArray(bit_count, 0)
        for targetIndex, sourceIndex in enumerate(range(start, stop, step)):
            result[targetIndex] = self[sourceIndex]
        
        return result

    def _set(self, index) -> 'None':
        self.bits |= (1 << index)

    def _unset(self, index) -> 'None':
        self.bits &= (~(1 << index))

    def _circular_shift(self: 'BitArray', amount: 'int') -> 'BitArray':
        result = BitArray.empty(self.size)
        
        for source in range(result.size):
            target = (source + amount) % result.size
            result[target] = self[source]

        return result

    def _unpack_silce(self, slice: 'slice') -> 'Tuple[int, int, int]':
        start, stop, step = slice.start or 0, slice.stop or self.size, slice.step or 1
        self._assert_index_within_range(start)
        self._assert_index_within_range(stop)
        start, stop = (stop - 1, start - 1) if step < 0 else (start, stop)
        return start, stop, step

    def _assert_index_within_range(self, index: 'int'):
        assert index >= 0 and index <= self.size

    def _assert_value_within_range(self, value: 'int'):
        assert value == 0 or value == 1
    

class BitArrayIterator:

    def __init__(self, bit_array: 'BitArray') -> 'None':
        self.bit_array = bit_array
        self.index = 0
    
    def __next__(self) -> 'int':
        if self.index == len(self.bit_array):
            raise StopIteration
        
        bit = self.bit_array[self.index]
        self.index += 1
        return bit

