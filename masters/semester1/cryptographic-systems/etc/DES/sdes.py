from pydoc import plain
from typing import List
from bitarray import BitArray

# sauce: https://terenceli.github.io/assets/file/mimaxue/SDES.pdf

P10 = [2, 4, 1, 6, 3, 9, 0, 8, 7, 5]
P8 = [5, 2, 6, 3, 7, 4, 9, 8]
P4 = [1, 3, 2, 0]
IP8 = [1, 5, 2, 0, 3, 7, 4, 6]
IP8_R = [3, 0, 2, 4, 6, 1, 7, 5]
EP =  [3, 0, 1, 2, 1, 2, 3, 0]

def permute(permutation: 'List[int]', bits: 'BitArray') -> 'BitArray':
    result = BitArray.empty(len(permutation))
    for targetIndex, sourceIndex in enumerate(permutation):
        result[targetIndex] = bits[sourceIndex]
    return result

S0 = [
    [BitArray(2, 0b01), BitArray(2, 0b00), BitArray(2, 0b11), BitArray(2, 0b10)],
    [BitArray(2, 0b11), BitArray(2, 0b10), BitArray(2, 0b01), BitArray(2, 0b00)],
    [BitArray(2, 0b00), BitArray(2, 0b10), BitArray(2, 0b01), BitArray(2, 0b11)],
    [BitArray(2, 0b11), BitArray(2, 0b01), BitArray(2, 0b11), BitArray(2, 0b10)]
]

S1 = [
    [BitArray(2, 0b00), BitArray(2, 0b01), BitArray(2, 0b10), BitArray(2, 0b11)],
    [BitArray(2, 0b10), BitArray(2, 0b00), BitArray(2, 0b01), BitArray(2, 0b11)],
    [BitArray(2, 0b11), BitArray(2, 0b00), BitArray(2, 0b01), BitArray(2, 0b00)],
    [BitArray(2, 0b10), BitArray(2, 0b01), BitArray(2, 0b00), BitArray(2, 0b11)]
]

def s(source: 'List[List[BitArray]]', bits: 'BitArray') -> 'BitArray':
    row = bits[0] * 2 + bits[3]
    column = bits[1] * 2 + bits[2]
    return source[row][column]

def generate_subkeys(key: 'BitArray') -> 'List[BitArray]':
    assert len(key) == 10
    key = permute(P10, key)
    left, right = key[:5], key[5:]

    result = []
    for offset in range(2):
        left, right = left << offset, right << offset
        key = permute(P8, left + right)
        result.append(key)

    return result

def encrypt(plaintext: 'BitArray', subkeys: 'List[BitArray]') -> 'BitArray':
    plaintext = permute(IP8, plaintext)
    left, right = plaintext[:4], plaintext[4:]
    ep = permute(EP, right) ^ subkeys[0]
    ep_left, ep_right = s(S0, ep[:4]), s(S1, ep[4:])
    p4 = permute(P4, ep_left + ep_right)
    left = left ^ p4
    left, right = right, left
    ep = permute(EP, right) ^ subkeys[1]
    ep_left, ep_right = s(S0, ep[:4]), s(S1, ep[4:])
    p4 = permute(P4, ep_left + ep_right)
    left = left ^ p4
    return permute(IP8_R, left + right)


key = BitArray(10, 0b0111100011)
subkeys = generate_subkeys(key)
for subkey in subkeys:
    print("Subkey:", subkey)

plaintext = BitArray(8, 0b00010100)
ciphertext = encrypt(plaintext, subkeys)

print("       Key:", key)
print(" Plaintext:", plaintext)
print("Ciphertext:", ciphertext)
