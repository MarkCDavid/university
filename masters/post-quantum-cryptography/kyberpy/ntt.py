from parameters import PARAMETERS
from utility import to_signed_short
from kmath import n_1_bits
import numpy as np
from extendedeuclidian import moduloInverse


def br7(source):
    target = ~n_1_bits(7)
    for _ in range(7):
        target = target | (source & 1)
        target = target << 1
        source = source >> 1
    return target

ROOT_OF_UNITY = 17
ZETAS = [0] * PARAMETERS.n

for i in range(PARAMETERS.n // 2):
    ZETAS[i] = pow(ROOT_OF_UNITY, i, PARAMETERS.q)

# print(ZETAS)

# TREE = [
#   0, 64, 32, 96, 16, 80, 48, 112, 8, 72, 40, 104, 24, 88, 56, 120,
#   4, 68, 36, 100, 20, 84, 52, 116, 12, 76, 44, 108, 28, 92, 60, 124,
#   2, 66, 34, 98, 18, 82, 50, 114, 10, 74, 42, 106, 26, 90, 58, 122,
#   6, 70, 38, 102, 22, 86, 54, 118, 14, 78, 46, 110, 30, 94, 62, 126,
#   1, 65, 33, 97, 17, 81, 49, 113, 9, 73, 41, 105, 25, 89, 57, 121,
#   5, 69, 37, 101, 21, 85, 53, 117, 13, 77, 45, 109, 29, 93, 61, 125,
#   3, 67, 35, 99, 19, 83, 51, 115, 11, 75, 43, 107, 27, 91, 59, 123,
#   7, 71, 39, 103, 23, 87, 55, 119, 15, 79, 47, 111, 31, 95, 63, 127
# ];

# ZETAS3 = [ZETAS2[x] for x in TREE]

# print(ZETAS)
# print(ZETAS2)
# print(ZETAS3)




# U=x [ j ] ;
# V=modmul ( x [ j+t ] , S ) ;
# x [ j ] = (U+V)%q ;
# x [ j+t ] = (U+q−V)%q ;

def ntt(polynomial):
    result = [0] * PARAMETERS.n
    for i in range(0, PARAMETERS.n // 2, 2):
        for j in range(PARAMETERS.n // 2):
            ZETAX = pow(ROOT_OF_UNITY, (2 * br7(i) + 1)*j, PARAMETERS.q)
            result[i + 0] += polynomial[2 * j + 0] * ZETAX
            result[i + 1] += polynomial[2 * j + 1] * ZETAX
            result[PARAMETERS.n // 2 + i + 0] += PARAMETERS.q - polynomial[2 * j + 0] * ZETAX
            result[PARAMETERS.n // 2 + i + 1] += PARAMETERS.q - polynomial[2 * j + 1] * ZETAX

    return [x % PARAMETERS.q for x in result]


def ntt_recursive(P, k):
    n = len(P)
    if n == 1:
        return P
    Pe, Po = P[0::2], P[1::2]
    ye, yo = ntt_recursive(Pe, k + 1), ntt_recursive(Po, k + 1)
    y = [0] * n
    for j in range(n//2):
        ZETAX = pow(ROOT_OF_UNITY, (2 * br7(k) + 1)*j, PARAMETERS.q) % PARAMETERS.q
        y[j] = (ye[j] + ZETAX*yo[j]) % PARAMETERS.q
        y[j + n//2] = (ye[j] - ZETAX*yo[j]) % PARAMETERS.q
    return y


def ntt2(signal):
    N = len(signal)
    zeta = 17
    zeta_powers = [((zeta ** x) % PARAMETERS.q) for x in range(N)]
    return [
        sum(
            signal[n] * zeta_powers[(n * f) % N]
            for n 
            in range(N)
        ) 
        for f 
        in range(N)
    ]