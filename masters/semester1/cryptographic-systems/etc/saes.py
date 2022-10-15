from typing import List
from bitarray2 import BitArray2

substitution_box = {
    BitArray2.fromBitString("0000"): BitArray2.fromBitString("1001"),
    BitArray2.fromBitString("0001"): BitArray2.fromBitString("0100"),
    BitArray2.fromBitString("0010"): BitArray2.fromBitString("1010"),
    BitArray2.fromBitString("0011"): BitArray2.fromBitString("1011"),
    BitArray2.fromBitString("0100"): BitArray2.fromBitString("1101"),
    BitArray2.fromBitString("0101"): BitArray2.fromBitString("0001"),
    BitArray2.fromBitString("0110"): BitArray2.fromBitString("1000"),
    BitArray2.fromBitString("0111"): BitArray2.fromBitString("0101"),
    BitArray2.fromBitString("1000"): BitArray2.fromBitString("0110"),
    BitArray2.fromBitString("1001"): BitArray2.fromBitString("0010"),
    BitArray2.fromBitString("1010"): BitArray2.fromBitString("0000"),
    BitArray2.fromBitString("1011"): BitArray2.fromBitString("0011"),
    BitArray2.fromBitString("1100"): BitArray2.fromBitString("1100"),
    BitArray2.fromBitString("1101"): BitArray2.fromBitString("1110"),
    BitArray2.fromBitString("1110"): BitArray2.fromBitString("1111"),
    BitArray2.fromBitString("1111"): BitArray2.fromBitString("0111")
}

class KeySchedule:

    def __init__(self: 'KeySchedule', key: 'BitArray2') -> None:
        word1 = key[0:8]
        word2 = key[8:16]
        word3 = word1 ^ KeySchedule.round(word2, BitArray2.fromBitString("1000"))
        word4 = word2 ^ word3
        word5 = word3 ^ KeySchedule.round(word4, BitArray2.fromBitString("0011"))
        word6 = word4 ^ word5

        self.keys = [
            word1 + word2,
            word3 + word4,
            word5 + word6
        ]

    def key(self: 'KeySchedule', index: 'int') -> 'BitArray2':
        return self.keys[index]

    @staticmethod
    def round(word: 'BitArray2', constant: 'BitArray2'):
        n0, n1 = word[:4], word[4:]
        n0, n1 = substitution_box[n1], substitution_box[n0]
        n0, n1 = n0 ^ constant, n1
        return n0 + n1

class Nibbles:
    @staticmethod
    def fromBitArray(bitArray: 'BitArray2') -> 'Nibbles':
        return Nibbles([bitArray[0:4], bitArray[4:8], bitArray[8:12], bitArray[12:16]])

    def toBitArray(self: 'Nibbles') -> 'BitArray2':
        return self.nibbles[0] + self.nibbles[1] + self.nibbles[2] + self.nibbles[3]

    def __init__(self: 'Nibbles', nibbles: 'List[BitArray2]') -> None:
        self.nibbles: 'List[BitArray2]' = nibbles

    def shift_row(self: 'Nibbles') -> 'Nibbles':
        return Nibbles([
            self.nibbles[0], 
            self.nibbles[3], 
            self.nibbles[2], 
            self.nibbles[1]
        ])

    def substitute(self: 'Nibbles') -> 'Nibbles':
        return Nibbles([
            substitution_box[self.nibbles[0]], 
            substitution_box[self.nibbles[1]], 
            substitution_box[self.nibbles[2]], 
            substitution_box[self.nibbles[3]]
        ])

    def mix_columns(self: 'Nibbles') -> 'Nibbles':
        columns = self.toBitArray()
        return Nibbles.fromBitArray(BitArray2.fromIntegerArray([
                columns[0] ^ columns[6], 
                columns[1] ^ columns[4] ^ columns[7], 
                columns[2] ^ columns[4] ^ columns[5], 
                columns[3] ^ columns[5],
                
                columns[2] ^ columns[4], 
                columns[0] ^ columns[3] ^ columns[5], 
                columns[0] ^ columns[1] ^ columns[6], 
                columns[1] ^ columns[7],

                columns[8] ^ columns[14], 
                columns[9] ^ columns[12] ^ columns[15], 
                columns[10] ^ columns[12] ^ columns[13], 
                columns[11] ^ columns[13],

                columns[10] ^ columns[12], 
                columns[8] ^ columns[11] ^ columns[13], 
                columns[8] ^ columns[9] ^ columns[14], 
                columns[9] ^ columns[15]
        ]))

    def __xor__(self: 'Nibbles', other: 'BitArray2') -> 'Nibbles':
        return Nibbles.fromBitArray(self.toBitArray() ^ other)

    def __str__(self: 'Nibbles') -> 'str':
        return str(self.toBitArray())
        

def encrypt(plaintext: 'BitArray2', key: 'BitArray2') -> 'BitArray2':
    key_schedule: KeySchedule = KeySchedule(key)
    nibbles: Nibbles = Nibbles.fromBitArray(plaintext)
    nibbles ^= key_schedule.key(0)
    nibbles = nibbles.substitute()
    nibbles = nibbles.shift_row()
    nibbles = nibbles.mix_columns()
    nibbles ^= key_schedule.key(1)
    nibbles = nibbles.substitute()
    nibbles = nibbles.shift_row()
    nibbles ^= key_schedule.key(2)
    return nibbles.toBitArray()


if __name__ == "__main__":
    plaintext = BitArray2.fromBitString("0110111101101011")
    key = BitArray2.fromBitString("1010011100111011")
    expected = BitArray2.fromBitString("0000011100111000")

    result = encrypt(plaintext, key)

    print(f"     Got: {result}")
    print(f"Expected: {expected}")
    print(f"    Pass: {result == expected}")