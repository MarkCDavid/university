from functools import reduce
from typing import List, Callable
from bitarray import BitArray

# sauce: https://terenceli.github.io/assets/file/mimaxue/SDES.pdf

def permute(permutation: 'List[int]', bits: 'BitArray') -> 'BitArray':
    result = BitArray.empty(len(permutation))
    for targetIndex, sourceIndex in enumerate(permutation):
        result[targetIndex] = bits[sourceIndex]
    return result

class FeistelCipher:
    
    def __init__(self, block_size: 'int', rounds: 'int') -> None:
        self.block_size = block_size
        self.rounds = rounds

    def encrypt(self, plaintext: 'BitArray', key: 'BitArray') -> 'BitArray':
        return self._to_ciphertext(
                    self._encrypt(block) 
                    for block 
                    in self._blocks(plaintext))

    def decrypt(self, plaintext: 'BitArray', key: 'BitArray') -> 'BitArray':
        return self._to_ciphertext(
                    self._decrypt(block) 
                    for block 
                    in self._blocks(plaintext))

    def function(self, block: 'BitArray', _round: 'int') -> 'BitArray':
        return block

    def _to_ciphertext(self, blocks: 'List[BitArray]') -> 'BitArray':
        _sum = lambda left, right: left + right
        return reduce(_sum, blocks, BitArray.empty(0))

    def _blocks(self, plaintext: 'BitArray') -> 'List[BitArray]':
        assert len(plaintext) % self.block_size == 0   
        
        return [plaintext[ block_start : block_start + self.block_size] 
                for block_start 
                in range(0, len(plaintext), self.block_size)]
    
    def _encrypt(self, block: 'BitArray') -> 'BitArray':
        for _round in range(self.rounds):
            block = self._round(block, _round)
        return block

    def _decrypt(self, block: 'BitArray') -> 'BitArray':
        for _round in reversed(range(self.rounds)):
            block = self._round(block, _round)
        return block

    def _round(self, plaintext: 'BitArray', _round: 'int') -> 'BitArray':
        left, right = plaintext.split()
        return right + (left ^ self.function(right, _round))


class SDESSubkeyGenerator:

    def __init__(self, key: 'BitArray') -> 'None':
        assert len(key) == 10
        self.key = key

    def get_subkey(self, _round: 'int') -> 'BitArray':
        key = self._p10(self.key)
        left, right = key.split() 

        for offset in range(_round + 1):
            left, right = left << (offset + 1), right << (offset + 1)
            key = self._p8(left + right)

        return key

    def _p10(self, bits: 'BitArray') -> 'BitArray':
        return permute([2, 4, 1, 6, 3, 9, 0, 8, 7, 5], bits)
        
    def _p8(self, bits: 'BitArray') -> 'BitArray':
        return permute([5, 2, 6, 3, 7, 4, 9, 8], bits)

class SDES(FeistelCipher):

    def __init__(self) -> 'None':
        super().__init__(8, 2)
        self.keygen = None
        self.S0 = self._construct_S([["01", "00", "11", "10"],
                                     ["11", "10", "01", "00"],
                                     ["00", "10", "01", "11"],
                                     ["11", "01", "11", "10"]])

        self.S1 = self._construct_S([["00", "01", "10", "11"],
                                     ["10", "00", "01", "11"],
                                     ["11", "00", "01", "00"],
                                     ["10", "01", "00", "11"]])

    def encrypt(self, plaintext: 'BitArray', key: 'BitArray') -> 'BitArray':
        self.keygen = SDESSubkeyGenerator(key)
        return super().encrypt(plaintext, key)

    def decrypt(self, plaintext: 'BitArray', key: 'BitArray') -> 'BitArray':
        self.keygen = SDESSubkeyGenerator(key)
        return super().decrypt(plaintext, key)

    def function(self, block: 'BitArray', _round: 'int') -> 'BitArray':
        block = self._ep(block)
        block = block ^ self.key(_round) 
        block = self._s0(block.left()) + self._s1(block.right()) 
        block = self._p4(block)
        return block
    
    def key(self, _round: 'int') -> 'BitArray':
        return self.keygen.get_subkey(_round)

    def _encrypt(self, block: 'BitArray') -> 'BitArray':
        block = self._ip8(block)
        block = super()._encrypt(block)
        return self._ip8_reverse(block.right() + block.left())

    def _decrypt(self, block: 'BitArray') -> 'BitArray':
        block = self._ip8(block)
        block = super()._decrypt(block)
        return self._ip8_reverse(block.right() + block.left())

    def _ip8(self, bits: 'BitArray') -> 'BitArray':
        return permute([1, 5, 2, 0, 3, 7, 4, 6], bits)

    def _ip8_reverse(self, bits: 'BitArray') -> 'BitArray':
        return permute([3, 0, 2, 4, 6, 1, 7, 5], bits)

    def _ep(self, bits: 'BitArray') -> 'BitArray':
        return permute([3, 0, 1, 2, 1, 2, 3, 0], bits)

    def _p4(self, bits: 'BitArray') -> 'BitArray':
        return permute([1, 3, 2, 0], bits)

    def _s0(self, bits: 'BitArray') -> 'BitArray':
        return self._s(self.S0, bits)

    def _s1(self, bits: 'BitArray') -> 'BitArray':
        return self._s(self.S1, bits)

    def _s(self, s: 'List[List[BitArray]]', bits: 'BitArray') -> 'Tuple[int, int]':
        row, column = (bits[0] * 2 + bits[3]), (bits[1] * 2 + bits[2])
        return s[row][column]

    def _construct_S(self, bit_strings: 'List[List[str]]') -> 'List[List[BitArray]]':
        return [
                [
                 BitArray.fromBitString(column) 
                 for column 
                 in row
                ] 
                for row 
                in bit_strings
               ] 


def testcase(expected: 'BitArray', got: 'BitArray'):
    print(f"Expected: {expected}\nGot: {got}\nPassed: {expected == got}\n")

def simple_test():
    plaintext = BitArray.fromBitString("00101000")
    key = BitArray.fromBitString("1100011110")
    expected = BitArray.fromBitString("10001010")
    got = SDES().encrypt(plaintext, key)
    testcase(expected, got)

def decrypt_test():
    ciphertext = BitArray.fromBitString("10001010")
    key = BitArray.fromBitString("1100011110")
    expected = BitArray.fromBitString("00101000")
    got = SDES().decrypt(ciphertext, key)
    testcase(expected, got)

def text_test():
    plaintext = BitArray.fromString("Hello, World!", "utf-8")
    key = BitArray.fromBitString("1100011110")
    expected = BitArray.fromBitString("01100100110010000000110100001101101111110100011001111111011101111011111100111100000011010010101011011001")
    got = SDES().encrypt(plaintext, key)
    testcase(expected, got)

def text_decrypt_test():
    ciphertext = BitArray.fromBitString("01100100110010000000110100001101101111110100011001111111011101111011111100111100000011010010101011011001")
    key = BitArray.fromBitString("1100011110")
    expected = BitArray.fromString("Hello, World!", "utf-8")
    got = SDES().decrypt(ciphertext, key)
    testcase(expected, got)

simple_test()
decrypt_test()
text_test()
text_decrypt_test()
