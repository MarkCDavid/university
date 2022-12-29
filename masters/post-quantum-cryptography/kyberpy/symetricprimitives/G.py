from utility import to_signed_byte
from typing import List, Tuple
from parameters import PARAMETERS
from Crypto.Hash import SHA3_512
from Crypto.Random import get_random_bytes

# REFERENCE: CRYSTALS-Kyber, Symmetric primitives, p. 5
# URL: https://pq-crystals.org/kyber/data/kyber-specification-round3-20210804.pdf

# Hash Function G (Seed Generator Function)
# input: bytearray
# output: bytearray, bytearray

# TODO(Aurimas): Although the algorithm uses function G(bytearray),
#                I feel like it's not descriptive enough. Figure out
#                a descriptive way to relate it to the documentation?


# This function generates two seeds (public and noise), by usage 
# of random bytes.
def random_bytes() -> 'bytes':
    if PARAMETERS._static:
        return bytearray(value & 0xFF for value in PARAMETERS._static_seed)
    return get_random_bytes(PARAMETERS.seed_size)

def generate_seed() -> 'Tuple[List[int], List[int]]':
    seed = [
        to_signed_byte(byte) 
        for byte 
        in SHA3_512.new(random_bytes()).digest()
    ]
    return (
        seed[0                    :     PARAMETERS.seed_size], 
        seed[PARAMETERS.seed_size : 2 * PARAMETERS.seed_size]
    )