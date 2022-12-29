from typing import List
from bitarray import BitArray
from utility import BitStream
from parameters import PARAMETERS
from symetricprimitives.XOF import XOF

# Given a byte stream, generate matrix A in NTT domain.
# Transposed matrix is generated simply by providing
# the indexes to the XOF in a different order.
def generate_A(seed: "List[int]"):
    return [[parse_polynomial(XOF(seed, j, i)) for j in range(0, PARAMETERS.k)] for i in range(0, PARAMETERS.k)]


def generate_A_transposed(seed: "List[int]"):
    return [[parse_polynomial(XOF(seed, i, j)) for j in range(0, PARAMETERS.k)] for i in range(0, PARAMETERS.k)]


## REFERENCE
## https://pq-crystals.org/kyber/data/kyber-specification-round3-20210804.pdf
## Algorithm 1

# Parses a uniformly random distribution into a polynomial.
# input: bitstream by XOF
# output: polynomial coefficient array in NTT domain [^0, ^1, ^2...]
def parse_polynomial(xof: "BitArray") -> "List[int]":
    result = rejection_sampling(xof.slice_bytes(0, 504), PARAMETERS.n)

    # If we failed to generate a required amount of coefficients
    # using rejection sampling, continue using the tail end of XOF
    # bitstream to perform additional rejection samplings to generate
    # required number of coefficients.
    while len(result) < PARAMETERS.n:
        auxillary = rejection_sampling(xof.slice_bytes(504, 168), PARAMETERS.n - len(result))
        result.extend(auxillary)
    return result


# READ_COUNT indicates number of bits that we need to read from a bitstream
# to construct an integer for rejection sampling.

# The maximum value for 11 bit number is 2048 (2^11), while the maximum
# value for 12 bit number is 4096 (2^12). As Kyber uses q = 3329, we are
# selecting to read 12 bits as it's the smallest number of bits we need
# to be able to generate numbers up to q.
READ_COUNT = 12

# While actual Kyber implementation uses byte arrays, we use bit arrays
# which simplifies the implementation of rejection sampling.
# The core idea is this - if we could read only one byte, we would.
# Unfortunetaly, as we require 12 bits, we need to read at least 2 bytes
# (8 bits/byte * 2 byte = 16 bits). Additionally, we would waste 4 bits
# (16 - 12 = 4), as such we need to take a total of 3 bytes.
# As we are using bit arrays, we can forgo such construction.
def rejection_sampling(bits: "BitArray", count: "int") -> "List[int]":
    result = []
    stream = BitStream(bits)
    while len(result) < count and stream.can_read(READ_COUNT):
        sample = stream.read(READ_COUNT).bits
        if sample < PARAMETERS.q:
            result.append(sample)

    return result


# A construction where we always read 24 bits (3 bytes) and append the values.
# It is more closely related to the algorithm implementation within
# KYBER documentation.
def __deprecated__rejection_sampling(bits: "BitArray", length: "int"):
    result = []
    stream = BitStream(bits)
    while len(result) < length and stream.can_read(24):
        d1 = stream.read(12).bits
        if d1 < PARAMETERS.q:
            result.append(d1)

        d2 = stream.read(12).bits
        if len(result) < length and d2 < PARAMETERS.q:
            result.append(d2)

    return result
