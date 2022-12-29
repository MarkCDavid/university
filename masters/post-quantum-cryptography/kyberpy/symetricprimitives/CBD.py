from typing import List
from bitarray import BitArray
from parameters import PARAMETERS

# REFERENCE: CRYSTALS-Kyber, Symmetric primitives, p. 5
# URL: https://pq-crystals.org/kyber/data/kyber-specification-round3-20210804.pdf

# Centered Binomial Distribution (CBD)
# input: bytearray, byte
# output: bytearray


# The noise polynomial (a polynomial with small values) is calculated
# by generating some noise vector, adding `eta` number of bits and
# subtracting another `eta` bits from the generated noise.
#
# `eta` limits the size of the polynomial coefficients.
def CBD(eta: "int", noise: "bytes") -> "List[int]":
    return [
        sum_consecutive_bits_by_signs(BitArray.fromBytes(noise), offset, get_signs(eta)) for offset in get_offsets(eta)
    ]


# When sampling a coefficient for a noise polynomial, the calculation is
# adding first n/2 and subtracting the next n/2 censecutive bits from the
# pseudo-random noise generator function. Meaning, if we had 001101 with
# eta = 3, the polynomial coefficient for that index would be calculated
# as 1 + 0 + 1 - 1 - 0 - 0;
#
# Expanding the example into Python 'bits' of the bit array would have
# values [1, 0, 1, 1, 0, 0] and 'signs' would have values [1, 1, 1, -1, -1, -1].
# This way, the first 3 bits are added, and the next 3 bits are subtracted.
def sum_consecutive_bits_by_signs(bits: "BitArray", offset: "int", signs: "List[int]") -> "int":
    return sum(bits[offset + index] * sign for index, sign in enumerate(signs))


# Creates a list of offsets for coefficient calculations. During sum by
# signs calculation, we add first 'eta' bits, and then subtract the next
# 'eta' bits. As such, in total we must offset our sampling from the
# pseudo-random noise generator function by '2 * eta' for every coefficient.
def get_offsets(eta: "int") -> "List[int]":
    return [2 * eta * i for i in range(0, PARAMETERS.polynomial_coefficient_count)]


# Creates a list of signs for coefficient calculations. The first
# 'eta' signs will be positive, the next 'eta' signs will be negative.
# e.g:
# eta = 1 => [1, -1]
# eta = 4 => [1, 1, 1, 1, -1, -1, -1, -1]
def get_signs(eta: "int") -> "List[int]":
    return [*([1] * eta), *([-1] * eta)]
