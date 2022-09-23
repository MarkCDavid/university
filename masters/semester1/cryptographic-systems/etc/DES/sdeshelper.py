from typing import List, Tuple
from bitarray import BitArray

def _permute(permutation: 'List[int]', bits: 'BitArray') -> 'BitArray':
    result = BitArray.empty(len(permutation))
    for targetIndex, sourceIndex in enumerate(permutation):
        result[targetIndex] = bits[sourceIndex]
    return result

def _S(bit_strings: 'List[List[str]]') -> 'List[List[BitArray]]':
    return [[BitArray.fromBitString(column) for column in row] for row in bit_strings] 

def _s_row_col(bits: 'BitArray') -> 'Tuple[int, int]':
    return bits[0] * 2 + bits[3], bits[1] * 2 + bits[2]

_S0 = _S([["01", "00", "11", "10"], ["11", "10", "01", "00"], ["00", "10", "01", "11"], ["11", "01", "11", "10"]])
_S1 = _S([["00", "01", "10", "11"], ["10", "00", "01", "11"], ["11", "00", "01", "00"], ["10", "01", "00", "11"]])

def P10(bits: 'BitArray') -> 'BitArray':
    return _permute([2, 4, 1, 6, 3, 9, 0, 8, 7, 5], bits)
        
def P8(bits: 'BitArray') -> 'BitArray':
    return _permute([5, 2, 6, 3, 7, 4, 9, 8], bits)

def IP8(bits: 'BitArray') -> 'BitArray':
    return _permute([1, 5, 2, 0, 3, 7, 4, 6], bits)

def IP8_reverse(bits: 'BitArray') -> 'BitArray':
    return _permute([3, 0, 2, 4, 6, 1, 7, 5], bits)

def EP(bits: 'BitArray') -> 'BitArray':
    return _permute([3, 0, 1, 2, 1, 2, 3, 0], bits)

def P4(bits: 'BitArray') -> 'BitArray':
    return _permute([1, 3, 2, 0], bits)

def S0(bits: 'BitArray') -> 'BitArray':
    row, col = _s_row_col(bits)
    return _S0[row][col]

def S1(bits: 'BitArray') -> 'BitArray':
    row, col = _s_row_col(bits)
    return _S1[row][col]

def to_blocks(bits: 'BitArray', block_size: 'int' = 8) -> 'List[BitArray]':
    return [bits[block_start : block_start + block_size] 
            for block_start 
            in range(0, len(bits), block_size)]

def from_blocks(blocks: 'List[BitArray]') -> 'BitArray':
    bit_string = ''.join(str(block) for block in blocks)
    return BitArray.fromBitString(bit_string)

