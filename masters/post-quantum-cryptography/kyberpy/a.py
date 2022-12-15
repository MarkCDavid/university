
from bitarray import BitArray
from typing import List, Tuple
from Crypto.Hash import SHAKE128
from parameters import PARAMETERS
from utility import to_unsigned_byte, BitStream

def generate_A_matrix(seed: 'List[int]'):
    return [
        [
            generate_A_polynomial(seed, (i, j)) 
            for j 
            in range(0, PARAMETERS.k)
        ] 
        for i 
        in range(0, PARAMETERS.k)
    ]

def generate_A_polynomial(seed: 'List[int]', polynomial_index: 'Tuple[int, int]') -> 'List[int]':
    noise = get_noise(seed, polynomial_index)
    result = generate_uniform(BitArray.fromBytes(noise[0:504]), PARAMETERS.n)
    while len(result) < PARAMETERS.n:
        auxillary = generate_uniform(BitArray.fromBytes(noise[504:672]), PARAMETERS.n - len(result))
        result.extend(auxillary)
    result.extend([0] * (PARAMETERS.polynomial_coefficient_count - len(result)))
    return result

def generate_uniform(bits: 'BitArray', length: 'int'):
    result = []
    stream = BitStream(bits)
    while len(result) < length and stream.can_read(12):
        d1 = stream.read(12).bits
        if d1 < PARAMETERS.q:
            result.append(d1)

        d2 = stream.read(12).bits
        if len(result) < length and d2 < PARAMETERS.q:
            result.append(d2)

    return result

def get_noise(seed, index) -> 'bytes':
    shake128 = SHAKE128.new()
    shake128.update(bytearray(to_unsigned_byte(x) for x in seed))
    shake128.update(bytearray(index[::-1]))
    return bytes(to_unsigned_byte(byte) for byte in shake128.read(672))

