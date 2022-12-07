from typing import List
from constants import N, Q
from bytearray import BitArray, ByteArray
from modular_reductions import mod_p

def parse(byteArray: 'ByteArray') -> 'List[int]':
    a = [0] * N
    i, j = 0, 0
    while j < N:
        d1 = byteArray[i] + 256 * (mod_p(byteArray[i + 1], 16))
        d2 = (byteArray[i + 1] // 16) + (16 * byteArray[i + 2])
        if d1 < Q:
            a[j] = d1
            j += 1
        if d2 < Q and j < N:
            a[j] = d2
            j += 1
        i += 3
    return a


def cbd(byteArray: 'ByteArray') -> 'List[int]':
    f = [0] * 256
    eta = len(byteArray.bytes) // 64
    bitArray: BitArray = byteArray.toBits()
    for i in range(256):
        a = sum([bitArray[2 * i * eta + j] for j in range(0, eta)])
        b = sum([bitArray[2 * i * eta + eta + j] for j in range(0, eta)])
        f[i] = a - b
    return f

def decode(byteArray: 'ByteArray', l: 'int') -> 'List[int]':
    f = [0] * 256
    bitArray = byteArray.toBits()
    for i in range(256):
        f[i] = sum([bitArray[i*l + j] * (2**j) for j in range(0, l)])
    return f


        


print(cbd(ByteArray([234] * (64 * 3))))
