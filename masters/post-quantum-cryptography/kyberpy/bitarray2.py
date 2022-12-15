import numpy as np
from typing import List, Literal, Tuple, Union

def _fromByte(_byte: 'int') -> 'BitArray2':
    return BitArray2([
        (_byte >> offset) & 1 
        for offset 
        in range(8)
    ])

def _toByte(bits: 'BitArray2') -> 'int':
    return sum([
        bit * value 
        for bit, value 
        in zip(
            bits, 
            [2**x for x in range(8)]
        )
    ])

def _byteCount(integer: 'int') -> 'int':
    return (integer.bit_length() + 7) // 8

def _toBytes(integer: 'int', endianess: 'Literal["little", "big"]') -> 'int':
    return integer.to_bytes(_byteCount(integer), endianess)

def _unpack_silce(slice: 'slice', size: 'int') -> 'Tuple[int, int, int]':
    start = slice.start or 0
    stop = slice.stop or size
    step = slice.step or 1

    if step < 0:
        return stop - 1, start - 1, step
    
    return start, stop, step

class BitArray2:
    
    @staticmethod
    def empty(size: 'int') -> 'BitArray2':
        return BitArray2([0 for _ in range(size)])

    @staticmethod
    def fromIntegerArray(integerArray: 'List[int]') -> 'BitArray2':
        return BitArray2([0 if i == 0 else 1 for i in integerArray])
        
    @staticmethod
    def fromBitArray(bitArray: 'BitArray2') -> 'BitArray2':
        return BitArray2([bit for bit in bitArray.bits])

    @staticmethod
    def fromNumPyArray(numPyArray):
        return BitArray2([0 if x == 0 else 1 for x in numPyArray])

    @staticmethod
    def fromBitString(bitString: 'str') -> 'BitArray2':
        return BitArray2([int(bit) for bit in bitString])

    @staticmethod
    def fromString(string: 'str', encoding: 'str') -> 'BitArray2':
        return BitArray2.fromBytes(string.encode(encoding))

    @staticmethod
    def fromInteger(integer: 'int', endianess: 'Literal["little", "big"]') -> 'BitArray2':
        return BitArray2.fromBytes(_toBytes(integer, endianess))
        
    @staticmethod
    def fromBytes(_bytes: 'bytes', size: 'int' = None) -> 'BitArray2':
        if size is None:
            size = len(_bytes) * 8

        return sum(
            [
                _fromByte(byte) 
                for byte 
                in _bytes
            ],
            start=BitArray2.empty(0)
        )[:size]
        
    def rshift_proper(self: 'BitArray2', amount: 'int') -> 'BitArray2':
        return BitArray2([*[0]*amount, *(self[:-amount].bits)])

    def land(self: 'BitArray2', other: 'BitArray2') -> 'BitArray2':
        return BitArray2([x * y for x,y in zip(self.bits, other.bits)])


    def toNumPyArray(self: 'BitArray2'):
        return np.array(self.bits)

    def toBytes(self: 'BitArray2') -> 'bytes':
        return bytes([
            _toByte(self[byteIndex: min(byteIndex + 8, len(self))]) 
            for byteIndex 
            in range(0, len(self), 8)
        ])

    def toString(self: 'BitArray2', encoding: 'str') -> 'str':
        return self.toBytes().decode(encoding)

    def toInteger(self: 'BitArray2', endianess: 'Literal["little", "big"]') -> 'str':
        return int.from_bytes(self.toBytes(), endianess) 

    def __init__(self: 'BitArray2', bits: 'List[int]') -> None:
        self.bits = bits

    def __len__(self: 'BitArray2') -> 'int':
        return len(self.bits)

    def __eq__(self: 'BitArray2', other: 'BitArray2') -> 'bool':
        if len(self.bits) != len(other.bits):
            return False
        return all(l == r for l, r in zip(self.bits, other.bits))

    def __add__(self: 'BitArray2', other: 'BitArray2') -> 'BitArray2':
        return BitArray2(self.bits + other.bits)

    def __xor__(self: 'BitArray2', other: 'BitArray2') -> 'BitArray2':
        return BitArray2([l ^ r for l, r in zip(self.bits, other.bits)])

    def __lshift__(self: 'BitArray2', amount: 'int') -> 'BitArray2':
        return BitArray2([self[index - amount] for index in range(len(self))])

    def __rshift__(self: 'BitArray2', amount: 'int') -> 'BitArray2':
        return BitArray2([self[index + amount] for index in range(len(self))])

    def __setitem__(self: 'BitArray2', index: 'int', value: 'int') -> 'None':
        self.bits[index % len(self)] = value

    def __str__(self: 'BitArray2') -> 'str':
        return ''.join(str(bit) for bit in self.bits)

    def __repr__(self: 'BitArray2') -> 'str':
        return f"BitArray2({str(self.bits)})"
        
    def __hash__(self) -> int:
        return hash(str(self))

    def __getitem__(self: 'BitArray2', coordinate: 'Union[int, slice]') -> 'Union[int, BitArray2]':
        if isinstance(coordinate, int):
            return self.__getitem_index__(coordinate)

        if isinstance(coordinate, slice):
            return self.__getitem_slice__(coordinate)
        
        raise Exception()

    def __getitem_index__(self: 'BitArray2', index: 'int') -> 'int':
        return self.bits[index % len(self)]

    def __getitem_slice__(self: 'BitArray2', _slice: 'slice') -> 'BitArray2':
        start, stop, step = _unpack_silce(_slice, len(self))
        return BitArray2([self[index] for index in range(start, stop, step)])

    def __iter__(self) -> 'BitArray2Iterator':
        return BitArray2Iterator(self)


class BitArray2Iterator:

    def __init__(self, bit_array: 'BitArray2') -> 'None':
        self.bit_array = bit_array
        self.index = 0
    
    def __next__(self) -> 'int':
        if self.index == len(self.bit_array):
            raise StopIteration
        
        bit = self.bit_array[self.index]
        self.index += 1

        return bit